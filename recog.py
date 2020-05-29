########### Python Form Recognizer Async Analyze #############
import json
import time
from requests import get, post
import glob
import pandas as pd
from collections import defaultdict
import os
# Endpoint URL
endpoint = r"https://sundartestfr.cognitiveservices.azure.com/"
apim_key = 'fbe18834321a4cdaad14183351b9f178'
model_id = "4c875b76-bda5-41f6-a773-9c7d4940fc92"    #Labelled model
#"d52e6115-f3b9-44f2-9db8-6e7ac379eb10"
post_url = endpoint + "/formrecognizer/v2.0-preview/custom/models/%s/analyze" % model_id


path = 'F:\\Download\\Test\\'
#files = [f for f in glob.glob(path + "**/*.pdf", recursive=True)]
json_out={}
def Recognize(files):
	
	for index,file in enumerate(files, start=1):
		source = path+file
		print("file",str(index),": ",file,end="  ")
		params = {
			"includeTextDetails": True
		}

		headers = {
			# Request headers
			'Content-Type': 'application/pdf',
			'Ocp-Apim-Subscription-Key': apim_key,
		}
		#print(type(source))
		with open(source, "rb") as f:
			data_bytes = f.read()

		try:
			resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
			if resp.status_code != 202:
				print("POST analyze failed:\n%s" % json.dumps(resp.json()))
				quit()
			#print("POST analyze succeeded:\n%s" % resp.headers)
			get_url = resp.headers["operation-location"]
		except Exception as e:
			print("POST analyze failed:\n%s" % str(e))
			quit()

	
		
		n_tries = 15
		n_try = 0
		wait_sec = 5
		max_wait_sec = 60
		while n_try < n_tries:
			try:
				resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
				resp_json = resp.json()
				if resp.status_code != 200:
					print("GET analyze results failed:\n%s" % json.dumps(resp_json))
					quit()
				status = resp_json["status"]
				if status == "succeeded":
					#writefile(resp_json)
					#print("test1")
					#print("Analysis succeeded:\n%s" % json.dumps(resp_json))
					json_out.update({os.path.basename(file):json.dumps(resp_json)})
					break
				if status == "failed":
					print("Analysis failed:\n%s" % json.dumps(resp_json))
					break
				# Analysis still running. Wait and retry.
				time.sleep(wait_sec)
				n_try += 1
				wait_sec = min(2*wait_sec, max_wait_sec)     
			except Exception as e:
				msg = "GET analyze results failed:\n%s" % str(e)
				print(msg)
				break
		#print(json_out)
	return (json_out,path)
#print("\nJson Parsing==================================================================================================\n\n")

# dep_dd = defaultdict(list)

# for filename,text in json_out.items():
# 	data=eval(text)
# 	result={}
# 	for res in data['analyzeResult']['documentResults']:
# 		result.update(res)
# 	dep_dd['FileName'].append(filename)
# 	for i in result['fields']:
# 		dep_dd[i].append(result['fields'][i]['text'])
	
# df=pd.DataFrame(dep_dd)
# df.to_csv('file_name1.csv',index=False)
# #print(df)
