package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    TextView maintext;
    TextView nameText;
    Button changeButton;
    Button nameButton;
    EditText nameInput;
    String[] cycler;

    RadioButton zebraRad;
    RadioButton waterBuffRad;
    RadioButton giraffeRad;
    RadioButton meerkatRad;
    RadioButton chimpRad;
    RadioButton rhinoRad;
    RadioButton gazelleRad;
    RadioButton armaRad;

    ConstraintLayout photoLayout;
    ConstraintLayout arrowLayout;
    ArrayList<RadioButton> radios;
    boolean imageSet = false;
    int count = 0;
    String name = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        maintext = findViewById(R.id.maintext);
        nameText = findViewById(R.id.name_text);
        changeButton=findViewById(R.id.change_button);
        nameButton=findViewById(R.id.name_button);
        nameInput=findViewById(R.id.name_input);

        zebraRad = findViewById(R.id.radio_zebra);
        waterBuffRad =findViewById(R.id.radio_water_buffalo);
        giraffeRad = findViewById(R.id.radio_giraffe);
        meerkatRad = findViewById(R.id.radio_meerkat);
        chimpRad = findViewById(R.id.radio_chimp);
        rhinoRad = findViewById(R.id.radio_rhino);
        gazelleRad = findViewById(R.id.radio_gazelle);
        armaRad = findViewById(R.id.radio_armadillo);

        photoLayout = findViewById(R.id.photo_layout);
        arrowLayout = findViewById(R.id.arrow_layout);

        radios = new ArrayList<>();
        radios.add(zebraRad);
        radios.add(waterBuffRad);
        radios.add(giraffeRad);
        radios.add(meerkatRad);
        radios.add(chimpRad);
        radios.add(rhinoRad);
        radios.add(gazelleRad);
        radios.add(armaRad);

        cycler = getResources().getStringArray(R.array.universe);

        for (RadioButton button : radios) {
            button.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                    if (isChecked) {
                        for (RadioButton b : radios) {
                            if (b.getId() != button.getId())
                                b.setChecked(false);
                        }
                    }
                }
            });
        }
        changeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (zebraRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.zebra);
                else if (waterBuffRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.water_buffalo);
                else if (giraffeRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.giraffe);
                else if (meerkatRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.meerkat);
                else if (chimpRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.chimpanzee);
                else if (rhinoRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.rhino);
                else if (gazelleRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.gazelle);
                else if (armaRad.isChecked())
                    photoLayout.setBackgroundResource(R.drawable.armadillo);
                imageSet = true;
            }
        });


        nameButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!nameInput.getText().toString().equals("") && imageSet) {
                    name = " " + nameInput.getText().toString();
                    arrowLayout.setBackgroundResource(R.drawable.arrow);
                }
                nameText.setText(name);
                if(imageSet)
                    nameInput.setText("");
            }
        });
    }
}