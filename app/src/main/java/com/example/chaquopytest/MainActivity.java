package com.example.chaquopytest;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
//import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.example.chaquopytest.databinding.ActivityMainBinding;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    ActivityMainBinding binding;

    ArrayList<String> arrayList_copies;
    ArrayList<Integer> arrayList_drawables;

    ArrayAdapter<String> arrayAdapter_copies;

//    TextView textView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding=ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());


//        textView = (TextView) findViewById(R.id.textview);

        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        Python py = Python.getInstance();

        PyObject pyObj = py.getModule("spot_counter");
        PyObject res = pyObj.callAttr("main");
//        textView.setText(res.toString());

        load_data();

        binding.spnCopies.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                binding.imgCopies.setImageResource(arrayList_drawables.get(position));
            }
            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });
    }

    public void load_data()
    {
        arrayList_copies=new ArrayList<>();
        arrayList_copies.add("30");
        arrayList_copies.add("100");
        arrayList_copies.add("300");
        arrayList_copies.add("1,000");
        arrayList_copies.add("3,000");
        arrayList_copies.add("10,000");
        arrayList_copies.add("30,000");
        arrayList_copies.add("100,000");

        arrayAdapter_copies=new ArrayAdapter<>(MainActivity.this,R.layout.mytextview, arrayList_copies);
        binding.spnCopies.setAdapter(arrayAdapter_copies);

        arrayList_drawables=new ArrayList<>();
        arrayList_drawables.add(R.drawable.a1);
        arrayList_drawables.add(R.drawable.a2);
        arrayList_drawables.add(R.drawable.a3);
        arrayList_drawables.add(R.drawable.a4);
        arrayList_drawables.add(R.drawable.a5);
        arrayList_drawables.add(R.drawable.a6);
        arrayList_drawables.add(R.drawable.a7);
        arrayList_drawables.add(R.drawable.a8);
    }
}