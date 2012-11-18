package com.triageteam.triage;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		new Connect().execute();
	}

	private static JSONArray getJSONfromURL(String url) {
		InputStream is = null;
		String result = "";
		JSONArray jArray = null;

		try {
			HttpClient httpclient = new DefaultHttpClient();
			// HttpPost httppost = new HttpPost(url);
			HttpGet httpGET = new HttpGet(url);
			HttpResponse response = httpclient.execute(httpGET);
			HttpEntity entity = response.getEntity();
			is = entity.getContent();
		} catch (Exception e) {
			Log.e("log_tag", "Error in http connection " + e.toString());
		}

		try {
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					is, "iso-8859-1"), 8);
			StringBuilder sb = new StringBuilder();
			String line = null;
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
			is.close();
			result = sb.toString();
		} catch (Exception e) {
			Log.e("log_tag", "Error converting result " + e.toString());
		}

		try {
			jArray = new JSONArray(result);
		} catch (JSONException e) {
			Log.e("log_tag", "Error parsing data " + e.toString());

		}

		return jArray;
	}

	void updateList(JSONArray finalArray) {

		ListView list = (ListView) findViewById(R.id.catastropheList);
		
		ArrayList<String> xxx = new ArrayList<String>();
		
		try  {
		
		for (int i = 0; i< finalArray.length(); i++) {
			//xxx.add(finalArray.getInt(i));
			JSONObject jo = (JSONObject) finalArray.get(i);
			xxx.add((String) jo.getString("description"));
			
		}
		
		}
		catch (Exception e) {
			// ignor
		}
		//for ()
		
		
		
//		String[] values = new String[] { "Android", "iPhone", "WindowsMobile",
//				  "Blackberry", "WebOS", "Ubuntu", "Windows7", "Max OS X",
//				  "Linux", "OS/2" };

				// First paramenter - Context
				// Second parameter - Layout for the row
				// Third parameter - ID of the TextView to which the data is written
				// Forth - the Array of data
				ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
				  android.R.layout.simple_list_item_1, android.R.id.text1, xxx);

				// Assign adapter to ListView
				list.setAdapter(adapter); 
		
		//list.u
		
	}
	
	
	private class Connect extends AsyncTask {
		ArrayList<HashMap<String, String>> myJSONList = new ArrayList<HashMap<String, String>>();

		@Override
		protected Object doInBackground(Object... params) {
			JSONArray finalArray = getJSONfromURL("http://184.73.4.189/triage/catastrophes/");

			try {
				for (int i = 0; i < finalArray.length(); i++) {
					HashMap<String, String> map = new HashMap<String, String>();
					JSONObject e = finalArray.getJSONObject(i);
					
					map.put("id",  String.valueOf(i));
					map.put("description", "Desc:" + e.getString("description"));
					
					myJSONList.add(map);
				}
				
			} catch (JSONException e) {
				Log.e("log_tag", "Error parsing data " + e.toString());
			}

			//Toast.makeText(MainActivity.this, "onPostExecute", Toast.LENGTH_LONG).show();
			
			doit(finalArray);
			
			return finalArray;
		}
		
		private void doit(final JSONArray finalArray) {
			MainActivity.this.runOnUiThread(new Runnable() {
			    public void run() {
			    	//titleProgress.setVisibility(View.INVISIBLE);
					//Toast.makeText(MainActivity.this, "onPostExecute", Toast.LENGTH_LONG).show();
			    	MainActivity.this.updateList(finalArray);
			    }
			});
		}
		
		protected void onPostExecute() {
			//doit(null);
			
			
		}
	}
}
