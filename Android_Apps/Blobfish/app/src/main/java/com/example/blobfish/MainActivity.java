package com.example.blobfish;

import androidx.appcompat.app.AppCompatActivity;

import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {

    EditText bpmInput;
    Button metrButton;
    Button stopButton;
    Button exitButton;
    Timer timer;
    MediaPlayer mp;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        bpmInput = findViewById(R.id.bpm_input);
        metrButton = findViewById(R.id.metronome_button);
        stopButton = findViewById(R.id.stop_button);
        exitButton = findViewById(R.id.exit_button);
        mp = MediaPlayer.create(MainActivity.this, R.raw.metrclick);
        timer = new Timer();

//        Runnable loopingRunnable = new Runnable() {
//            @Override
//            public void run() {
//                if (mp != null) {
//                    if (mp.isPlaying()) {
//                        mp.stop();
//                    }
//                    mp.start();
//                }
//            }
//        };

        metrButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int bpm = Integer.parseInt(bpmInput.getText().toString());
//                mp.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
//                    @Override
//                    public void onCompletion(MediaPlayer mp) {
//                        metrButton.postDelayed(loopingRunnable, 60 * 1000 / bpm);
//                    }
//                });
//                mp.start();
                timer.cancel();
                timer = new Timer();
                TimerTask task = new TimerTask() {
                    @Override
                    public void run() {
                        mp.start();
                    }
                };
                timer.schedule(task, 0, 60*1000/bpm);
            }
        });

            stopButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    timer.cancel();
//                        mp.stop();
                }
            });

            exitButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    timer.cancel();
                    finishAffinity();
                }
            });
    }
}