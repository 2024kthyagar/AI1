package com.example.fragments;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentTransaction;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements ContactFragment.OnItemSelectedListener{

    Button addButton;
    Button editButton;
    Button removeButton;
    EditText nameEdit;
    EditText phoneEdit;
    Button addChangeButton;
    Button editChangeButton;
    Button removeChangeButton;
    LinearLayout linearLayout;
    String selectedName="";
    Map<ContactFragment, Integer> idMap;
    int id = 1;
    boolean clickable = false;
    boolean removing = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        addButton = findViewById(R.id.add_button);
        editButton = findViewById(R.id.edit_button);
        removeButton = findViewById(R.id.remove_button);
        nameEdit = findViewById(R.id.name_edit);
        phoneEdit = findViewById(R.id.phone_edit);
        addChangeButton = findViewById(R.id.add_change_button);
        editChangeButton = findViewById(R.id.edit_change_button);
        removeChangeButton = findViewById(R.id.remove_change_button);
        linearLayout = findViewById(R.id.framelayout);
        idMap = new HashMap<>();

        addButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                nameEdit.setVisibility(View.VISIBLE);
                phoneEdit.setVisibility(View.VISIBLE);
                nameEdit.setText("");
                phoneEdit.setText("");
                addChangeButton.setVisibility(View.VISIBLE);
                addChangeButton.setEnabled(true);
            }
        });

        editButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                nameEdit.setVisibility(View.VISIBLE);
                phoneEdit.setVisibility(View.VISIBLE);
                editChangeButton.setVisibility(View.VISIBLE);
                editChangeButton.setEnabled(true);
                clickable = true;
            }
        });

        removeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                removeChangeButton.setVisibility(View.VISIBLE);
                removeChangeButton.setEnabled(true);
                clickable = true;
                removing = true;
            }
        });

        addChangeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String name = nameEdit.getText().toString();
                String phone = phoneEdit.getText().toString();

                StringBuilder phoneNum = new StringBuilder();
                for(int i=0; i<phone.length(); i++){
                    try{
                        phoneNum.append(Integer.parseInt(phone.substring(i, i + 1)));
                    }
                    catch(NumberFormatException e) {
                        continue;
                    }
                }
                phone = phoneNum.toString();
                if(phone.length()!=10){
                    phoneEdit.getText().clear();
                    phoneEdit.setHint("Invalid Number");
                }
                else if (name.length() <=0) {
                    nameEdit.getText().clear();
                    nameEdit.setHint("Invalid Name");
                }
                else {
                    nameEdit.setVisibility(View.INVISIBLE);
                    phoneEdit.setVisibility(View.INVISIBLE);
                    nameEdit.setText("");
                    phoneEdit.setText("");
                    addChangeButton.setVisibility(View.INVISIBLE);
                    addChangeButton.setEnabled(false);
                    nameEdit.setHint("Name");
                    phoneEdit.setHint("Phone Number");

                    phone = "("+phone.substring(0,3)+")-"+phone.substring(3,6)+"-"+phone.substring(6);

                    add_fragment(name, phone);
                }
            }
        });
        editChangeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (!selectedName.equals("")) {
                    String tag = selectedName;
                    String name = nameEdit.getText().toString();
                    String phone = phoneEdit.getText().toString();
                    ContactFragment contactFragment = (ContactFragment) getSupportFragmentManager().findFragmentByTag(tag);

                    StringBuilder phoneNum = new StringBuilder();
                    for (int i = 0; i < phone.length(); i++) {
                        try {
                            phoneNum.append(Integer.parseInt(phone.substring(i, i + 1)));
                        } catch (NumberFormatException e) {
                            continue;
                        }
                    }
                    phone = phoneNum.toString();
                    if (phone.length() != 10) {
                        phoneEdit.getText().clear();
                        phoneEdit.setHint("Invalid Number");
                    }
                    else if (name.length() <=0) {
                        nameEdit.getText().clear();
                        nameEdit.setHint("Invalid Name");
                    }
                    else {
                        nameEdit.setVisibility(View.INVISIBLE);
                        phoneEdit.setVisibility(View.INVISIBLE);
                        nameEdit.setText("");
                        phoneEdit.setText("");
                        editChangeButton.setVisibility(View.INVISIBLE);
                        editChangeButton.setEnabled(false);
                        nameEdit.setHint("Name");
                        phoneEdit.setHint("Phone Number");
                        clickable = false;
                        selectedName = "";

                        phone = "("+phone.substring(0,3)+")-"+phone.substring(3,6)+"-"+phone.substring(6);


                        replace_fragment(contactFragment, name, phone);
                    }
                }
            }
        });

        removeChangeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!selectedName.equals("")) {
                    String tag = selectedName;
                    ContactFragment contactFragment = (ContactFragment) getSupportFragmentManager().findFragmentByTag(tag);
                    remove_fragment(contactFragment);
                    removeChangeButton.setVisibility(View.INVISIBLE);
                    removeChangeButton.setEnabled(false);
                    clickable = false;
                    selectedName = "";
                    removing = false;
                }
            }
        });
    }

    @Override
    public void sendData(String n, String p) {
        nameEdit.setText(n);
        phoneEdit.setText(p);
    }

    public void changeFrag(View view) {
        if(clickable) {
            TextView nameText = view.findViewById(R.id.name_text);
            TextView phoneText = view.findViewById(R.id.phone_text);
            selectedName = nameText.getText().toString();
            if(!removing) {
                nameEdit.setText(nameText.getText().toString());
                phoneEdit.setText(phoneText.getText().toString());
            }
            else {
                for(ContactFragment fragment : idMap.keySet())
                    fragment.getView().setBackgroundColor(Color.TRANSPARENT);
                view.setBackgroundColor(getResources().getColor(R.color.red));
            }

        }
    }

    public void add_fragment(String name, String phone) {

        FrameLayout temp = new FrameLayout(this);//new FrameLayout for each entry
        linearLayout.addView(temp);//attach FrameLayout to LinearLayout
        temp.setId(id);//set the id number for the new FrameLayout
        // Begin the transaction
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        // add new fragment to the FrameLayout
        ContactFragment fragment = ContactFragment.newInstance(name, phone);
        ft.add(id, fragment, name);
        idMap.put(fragment, id);
        // or ft.add(R.id.your_placeholder, new FooFragment());
        // Complete the changes added above
        ft.commit();
        id++;

    }

    public void replace_fragment(ContactFragment fragment, String name, String phone) {
        id = idMap.get(fragment);
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ContactFragment newFragment = ContactFragment.newInstance(name, phone);
        ft.replace(id, newFragment, name);
        idMap.remove(fragment);
        idMap.put(newFragment, id);
        ft.commit();

    }

    public void remove_fragment(ContactFragment fragment) {
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.remove(fragment);
        idMap.remove(fragment);
        ft.commit();

    }
}