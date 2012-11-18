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
import android.widget.Toast;

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

			return finalArray;
		}
		
		protected void onPostExecute() {
			Toast.makeText(MainActivity.this, "onPostExecute", Toast.LENGTH_LONG).show();
		}
	}
}
