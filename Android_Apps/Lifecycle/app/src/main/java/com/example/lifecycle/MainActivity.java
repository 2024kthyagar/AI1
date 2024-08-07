package com.example.lifecycle;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.TextView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    String TAG = "com.example.lifecycle";
    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;
    ArrayList<TextView> restartTextViews;
    ArrayList<TextView> installTextViews;
    String[] formatStrings;
    ArrayList<Integer> restartValues;
    ArrayList<Integer> installValues;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        formatStrings = getResources().getStringArray(R.array.format_strings);

        restartValues = new ArrayList<>();
        installValues = new ArrayList<>();

        sharedPreferences = getSharedPreferences(TAG, MODE_PRIVATE);
        editor = sharedPreferences.edit();

        restartTextViews = new ArrayList<>();
        for(int id : new int[]{R.id.restart_create, R.id.restart_start, R.id.restart_resume, R.id.restart_pause, R.id.restart_stop, R.id.restart_restart, R.id.restart_destroy}) {
            restartTextViews.add(findViewById(id));
        }
        installTextViews = new ArrayList<>();
        for(int id : new int[]{R.id.install_create, R.id.install_start, R.id.install_resume, R.id.install_pause, R.id.install_stop, R.id.install_restart, R.id.install_destroy}) {
            installTextViews.add(findViewById(id));
        }

        //increment onCreate
        int restartCreateValue = Integer.parseInt(sharedPreferences.getString("restartValue0", "0"));
        editor.putString("restartValue0", restartCreateValue+1+"");
        int installCreateValue = Integer.parseInt(sharedPreferences.getString("installValue0", "0"));
        editor.putString("installValue0", installCreateValue+1+"");

        editor.apply();
        setInitialValues();


    }

    @Override
    protected void onStart() {
        super.onStart();
        int restartStartValue = Integer.parseInt(sharedPreferences.getString("restartValue1", "0"));
        editor.putString("restartValue1", restartStartValue+1+"");
        int installStartValue = Integer.parseInt(sharedPreferences.getString("installValue1", "0"));
        editor.putString("installValue1", installStartValue+1+"");
        editor.apply();
        setInitialValues();
    }

    @Override
    protected void onResume() {
        super.onResume();
        int restartResumeValue = Integer.parseInt(sharedPreferences.getString("restartValue2", "0"));
        editor.putString("restartValue2", restartResumeValue+1+"");
        int installResumeValue = Integer.parseInt(sharedPreferences.getString("installValue2", "0"));
        editor.putString("installValue2", installResumeValue+1+"");
        editor.apply();
        setInitialValues();
    }

    @Override
    protected void onPause() {
        super.onPause();
        int restartPauseValue = Integer.parseInt(sharedPreferences.getString("restartValue3", "0"));
        editor.putString("restartValue3", restartPauseValue+1+"");
        int installPauseValue = Integer.parseInt(sharedPreferences.getString("installValue3", "0"));
        editor.putString("installValue3", installPauseValue+1+"");
        editor.apply();
        setInitialValues();
    }

    @Override
    protected void onStop() {
        super.onStop();
        int restartStopValue = Integer.parseInt(sharedPreferences.getString("restartValue4", "0"));
        editor.putString("restartValue4", restartStopValue+1+"");
        int installStopValue = Integer.parseInt(sharedPreferences.getString("installValue4", "0"));
        editor.putString("installValue4", installStopValue+1+"");
        editor.apply();
        setInitialValues();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        for (int i=0; i<formatStrings.length; i++)
            editor.putString("restartValue"+i, "0");
        editor.putString("restartValue5", "1");
        int installRestartValue = Integer.parseInt(sharedPreferences.getString("installValue5", "0"));
        editor.putString("installValue5", installRestartValue+1+"");
        editor.apply();
        setInitialValues();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        int restartDestroyValue = Integer.parseInt(sharedPreferences.getString("restartValue6", "0"));
        editor.putString("restartValue6", restartDestroyValue+1+"");
        int installDestroyValue = Integer.parseInt(sharedPreferences.getString("installValue6", "0"));
        editor.putString("installValue6", installDestroyValue+1+"");
        editor.apply();
        setInitialValues();
    }

    private void setInitialValues()   {
        for (int i=0; i<formatStrings.length; i++){
            TextView t = restartTextViews.get(i);
//            t.setText(sharedPreferences.getString(t.getTag().toString(), String.format(formatStrings[i], ("0"))));
            t.setText(String.format(formatStrings[i], Integer.parseInt(sharedPreferences.getString("restartValue"+i, "0"))));
        }
        for (int i=0; i<formatStrings.length; i++){
            TextView t = installTextViews.get(i);
//            t.setText(sharedPreferences.getString(t.getTag().toString(), String.format(formatStrings[i], ("0"))));
            t.setText(String.format(formatStrings[i], Integer.parseInt(sharedPreferences.getString("installValue"+i, "0"))));
        }
    }
}