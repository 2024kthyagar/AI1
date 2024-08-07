package com.example.sharedprefs;

import android.content.SharedPreferences;
import android.graphics.Color;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.google.android.material.snackbar.Snackbar;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity  implements View.OnClickListener{
    String TAG = "com.example.sharedprefs";
    Button bRight, bLeft;
    TextView tLeft, tRight;
    SeekBar seekBar;
    TextView[] views;
    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;
    ConstraintLayout layout;
    int freq;

    long startTime, clicks;
    float cPS;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        layout = findViewById(R.id.layout);
        bRight=findViewById(R.id.botright_button);
        bLeft=findViewById(R.id.botleft_button);
        tLeft=findViewById(R.id.topleft_textview);
        tRight=findViewById(R.id.topright_textview);
        views= new TextView[]{bLeft, bRight, tLeft, tRight};
        seekBar=findViewById(R.id.seekbar);

        sharedPreferences = getSharedPreferences(TAG, MODE_PRIVATE);
        editor = sharedPreferences.edit();

        bRight.setOnClickListener(this);
        bLeft.setOnClickListener(this);
        tLeft.setOnClickListener(this);
        tRight.setOnClickListener(this);


        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int lastprogress;

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean b) {
                for (TextView t : views)
                    t.setTextSize(progress);
                int red = progress*5%4*80;
                int green = progress*7%6*50;
                int blue = progress%11*25;
                layout.setBackgroundColor(Color.rgb(red, green, blue));
                freq = progress+440;
                AudioTrack tone = generateTone(freq,250,5);
                tone.play();

            }


            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                lastprogress = seekBar.getProgress();
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                Snackbar snackbar = Snackbar.make(layout,
                        "Font size changed to: " + seekBar.getProgress() + "sp",
                        Snackbar.LENGTH_LONG);
                snackbar.setAction("UNDO",
                        new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {
                                seekBar.setProgress(lastprogress);
                                for (TextView t : views)
                                    t.setTextSize(lastprogress);
                                Snackbar.make(layout, "Font Size Reverted to " + seekBar.getProgress() + "sp",
                                        Snackbar.LENGTH_LONG).show();
                            }
                        });
                snackbar.setActionTextColor(Color.BLUE);
                View snackbarView = snackbar.getView();
                TextView snackText = snackbarView.findViewById(com.google.android.material.R.id.snackbar_text);
                snackText.setTextColor(Color.WHITE);
                snackbar.show();
            }
        });
        layout.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                editor.clear().apply();
                setInitialValues();
                return false;
            }
        });
        setInitialValues();
        startTime = System.currentTimeMillis();
    }

    private void setInitialValues() {
        for (TextView t : views)
            t.setText(sharedPreferences.getString(t.getTag().toString(), "0"));
        seekBar.setProgress(30);
    }

    @Override
    public void onClick(View view) {
        TextView t = (TextView) view;
        t.setText(""+(Integer.parseInt(t.getText().toString())+1));
        editor.putString(t.getTag().toString(), t.getText().toString());
        editor.apply();
        cPS = ++clicks/((float)(System.currentTimeMillis()-startTime)/1000);
        Toast.makeText( this, ""+cPS,Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        setInitialValues();
    }

    private AudioTrack generateTone(double freqHz, int durationMs, double volume)
    {
        if (volume > 1 || volume < 0){
            volume = 1; //will make sure it isn't too loud
        }
        int count = (int)(44100.0 * 2.0 * (durationMs / 1000.0)) & ~1;
        short[] samples = new short[count];
        for(int i = 0; i < count; i += 2){
            short sample = (short)(volume * Math.sin(2 * Math.PI * i / (44100.0 / freqHz)) * 0x7FFF);
            samples[i + 0] = sample;
            samples[i + 1] = sample;
        }
        AudioTrack track = new AudioTrack(AudioManager.STREAM_MUSIC, 44100,
                AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT,
                count * (Short.SIZE / 8), AudioTrack.MODE_STATIC);
        track.write(samples, 0, count);
        return track;
    }
}
