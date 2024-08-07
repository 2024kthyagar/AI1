package com.example.viewpager;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.fragment.app.Fragment;
import androidx.viewpager2.widget.ViewPager2;

import com.google.android.material.tabs.TabLayout;
import com.google.android.material.tabs.TabLayoutMediator;

import java.util.ArrayList;

public class MainFragment extends Fragment {
    ViewPager2 viewpager;
    int position;
    public static Fragment newInstance(ViewPager2 v, int pos) {
        MainFragment fragment = new MainFragment();
        fragment.viewpager = v;
        fragment.position = pos;
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_main, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        TabLayout tablayout = getActivity().findViewById(R.id.tab_layout);
        new TabLayoutMediator(tablayout, viewpager,
                (tab,position) -> tab.setText("House" + (position))
                ).attach();
        ArrayList<Integer> lst = new ArrayList<>();
        lst.add(R.drawable.table);
        lst.add(R.drawable.bed);
        lst.add(R.drawable.books);
        lst.add(R.drawable.desk);
        lst.add(R.drawable.kitchen);
        lst.add(R.drawable.piano);

        ConstraintLayout layout = view.findViewById(R.id.fragment_container);
        layout.setBackgroundResource(lst.get(position));
//        Button button = view.findViewById(R.id.pressme);
//        button.setText("EEEE");
    }

}
