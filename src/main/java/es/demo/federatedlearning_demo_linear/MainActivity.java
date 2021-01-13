
/*
Alejandro Aguilera Alcalde
10/01/2021
 */

package es.demo.federatedlearning_demo_linear;



import android.os.Environment;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

//import com.google.android.gms.common.util.ArrayUtils;

import org.tensorflow.Graph;
import org.tensorflow.Session;
import org.tensorflow.Tensor;
import org.tensorflow.Tensors;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.nio.FloatBuffer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Random;
import java.util.zip.Deflater;

import androidx.appcompat.app.AppCompatActivity;
import lecho.lib.hellocharts.model.Axis;
import lecho.lib.hellocharts.model.AxisValue;
import lecho.lib.hellocharts.model.Line;
import lecho.lib.hellocharts.model.LineChartData;
import lecho.lib.hellocharts.model.PointValue;
import lecho.lib.hellocharts.model.Viewport;
import lecho.lib.hellocharts.view.LineChartView;

import android.graphics.Color;
import android.os.Bundle;

import java.util.ArrayList;
import java.util.List;


//MODELO:  simple Linear Regressor: y = x * W + b

public class MainActivity extends AppCompatActivity {
    byte[] graphDef;
    byte[] variableAuxCheck;
    Session sess;
    Graph graph;
    File file1;
    File file;   //este file es el que se manda al servidor ~~~~
    File file_descargado;
    File textFile;
    ArrayList<String> pesos = new ArrayList<>();
    Tensor<String> checkpointPrefix;
    String checkpointDir;
    InputStream inputCheck;
    float num_epoch = 0;
    boolean isModelUpdated = false;
    int modelctr = 8005;
    ArrayList<Float> y_mejoras_w = new ArrayList<Float>();
    ArrayList<String> x_mejoras_w = new  ArrayList<String>();
    ArrayList<Float> y_mejoras_b = new  ArrayList<Float>();
    ArrayList<String> x_mejoras_b = new ArrayList<String>();
    int num= 0; //contador para el array de las graficas

    LineChartView lineChartView;
    LineChartView lineChartView2;



    TextView B;
    TextView W;
    TextView Wtest;
    TextView Btest;
    TextView Y;
    Button button ;
    EditText epochs;

    static {
        System.loadLibrary("tensorflow_inference");
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        file1 = new File(getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), "/file1prueba");
         setContentView(R.layout.activity_main);
      //  setContentView(R.layout.activity_main);
        InputStream inputStream;


        try {
            //Place the .pb file generated before in the assets folder and import it as a byte[] array

            inputStream = getAssets().open("graph5.pb");
            byte[] buffer = new byte[inputStream.available()];
            int bytesRead;
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                output.write(buffer, 0, bytesRead);
            }
            graphDef = output.toByteArray();  // ARRAY CON EL GRAPH
        } catch (IOException e) {
            e.printStackTrace();
        }
        //Create a variable of class org.tensorflow.Graph:
        Graph graph = new Graph();
        sess = new Session(graph);
        //load the graph from the graphdef
        graph.importGraphDef(graphDef);
        sess.runner().addTarget("init").run(); //INICIALIZAR EL GRAPH
        Toast.makeText(getApplicationContext(), "Initialized" + sess.toString(), Toast.LENGTH_SHORT).show();

        //VISTAS Y BOTONES

        W = (TextView) findViewById(R.id.W);
        B = (TextView) findViewById(R.id.B);
        Wtest = (TextView) findViewById(R.id.Wtest);
        Btest = (TextView) findViewById(R.id.Btest);
        button = (Button) findViewById(R.id.button);
        epochs = (EditText) findViewById(R.id.epochs);
        Y = (TextView) findViewById(R.id.Y);

        //mi boton de pruebas
        final Button buttonPruebas = (Button) findViewById(R.id.buttonPrueba);

        //graficas
        lineChartView  = findViewById(R.id.chart);
        lineChartView2  = findViewById(R.id.chart2);



        //BOTON RUN
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Funcionar_salida(1);
                //prueba

            }
        });
        //BOTON UPLOAD
        Button upload = findViewById(R.id.uploadWeights);
        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //    writeFileTest(); ////******* PRUEBA FICHERO TXT. funciona perfecto
                writeFileLinear();
                MyAsyncTask uploadWeights = new MyAsyncTask(MainActivity.this, file, "uploadWeights", new MyAsyncTask.AsyncResponse() {
                    @Override
                    public void processFinish(String result) {
                        Log.i("Output: uploadWeights", result);
                        Toast.makeText(MainActivity.this, "2 Weights Successfully Uploaded", Toast.LENGTH_SHORT).show();



                    }
                });
                uploadWeights.execute();

                Toast.makeText(MainActivity.this, "2 Weights updated", Toast.LENGTH_SHORT).show();
            }



        });



        //BOTON GETMODEL ***VERSION NORMAL***
        Button getModel = findViewById(R.id.getModel);
        getModel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MyAsyncTask isGlobalModelUpdated = new MyAsyncTask(MainActivity.this, file, "ismodelUpdated", new MyAsyncTask.AsyncResponse() {
                    @Override
                    public void processFinish(String result) {
                        //If True, get Global Model
                        MyAsyncTask getGlobalModel = new MyAsyncTask(MainActivity.this, file, "getModel", new MyAsyncTask.AsyncResponse() {
                            @Override
                            public void processFinish(String result) {
                                Log.i("Output: GetGlobalModel", result);
                            }
                        });
                        getGlobalModel.execute();
                        //  Toast.makeText(MainActivity.this, "Fetched Global Model Successfully", Toast.LENGTH_SHORT).show();
                        Log.i("Output: isModelUpdated", "Done");

                    }
                });
                isGlobalModelUpdated.execute();
                file_descargado = new File(getApplicationContext().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS).getAbsolutePath(), "graph_pesos");

                Toast.makeText(MainActivity.this, "se ha guardado el nuevo checkpoint", Toast.LENGTH_SHORT).show();
                //actualizo el etado del modelo.
                isModelUpdated = true;
            }
        });


        //BOTON PRUEBA Hasta guardar fichero weights.
        buttonPruebas.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                float n_epochs = Float.parseFloat(epochs.getText().toString());
                float num1 = (float) Math.random();
                num_epoch = n_epochs;
                int epochs = (int)n_epochs;
                // initializeGraphPrueba();


                if (isModelUpdated) {

                    initializeGraph_check();  //para restaurar el graph con los checkpoints actualizados.
                    isModelUpdated = false;
                }

                predictPrueba(num1);
                num++;
                trainPrueba(num1, epochs);
                Graficar_w();
                Graficar_b();





            }
        });





    }



    //***********
    //TRAINING THE MODEL ON-DEVICE
    //*********

    private float[] flattenedWeight(Tensor t) {
/*
        float[] flat = new float[(int) (t.shape()[0]) * (int) t.shape()[1]];
       float[][] arr = new float[(int) (t.shape()[0])][(int) t.shape()[1]];
        t.copyTo(arr);
        int x = 0;
        for (int i = 0; i < t.shape()[0]; i++) {
            for (int j = 0; j < t.shape()[1]; j++) {
               flat[x] = arr[i][j];
                x++;
            }
        }
       return flat;

    }
    */
        float[] flat = new float[0];

        t.copyTo(flat);


        return flat;

    }


    ////LAS PRUEBAS DEL BOTON PRUEBA
    //**
    // (i) Loading the model in the Android Application
    //**
    public void initializeGraphPrueba() {

        //To load the checkpoint, place the checkpoint files in the device and create a Tensor
        //to the path of the checkpoint prefix


        // si modelo updated se usa el checkpoints que he descargado del servidor. Si no, el del movil.
        if (isModelUpdated){



            try {

                inputCheck = getAssets().open("+checkpoints_name_1002-.ckpt.meta");

                byte[] buffer = new byte[inputCheck.available()];
                int bytesRead;
                ByteArrayOutputStream output = new ByteArrayOutputStream();
                while ((bytesRead = inputCheck.read(buffer)) != -1) {
                    output.write(buffer, 0, bytesRead);
                }
                variableAuxCheck = output.toByteArray();  // array con el checkpoint
            } catch (IOException e) {
                e.printStackTrace();
            }
            checkpointPrefix = Tensors.create((variableAuxCheck).toString());
        }

        else {
            try {
                //Place the .pb file generated before in the assets folder and import it as a byte[] array
                // hay que poner el .meta
                inputCheck = getAssets().open("checkpoint_name1.ckpt.meta");
                byte[] buffer = new byte[inputCheck.available()];
                int bytesRead;
                ByteArrayOutputStream output = new ByteArrayOutputStream();
                while ((bytesRead = inputCheck.read(buffer)) != -1) {
                    output.write(buffer, 0, bytesRead);
                }
                variableAuxCheck = output.toByteArray();  // array con el checkpoint
            } catch (IOException e) {
                e.printStackTrace();
            }
            checkpointPrefix = Tensors.create((variableAuxCheck).toString());
        }


        //Create a variable of class org.tensorflow.Graph:
        graph = new Graph();
        sess = new Session(graph);
        InputStream inputStream;
        try {

            if (isModelUpdated) {                                                  // ESTO ES ALGO TEMPORAL.
                inputStream = getAssets().open("graph_pesos.pb");
            }
            else {
                inputStream = getAssets().open("graph5.pb");
            }
            byte[] buffer = new byte[inputStream.available()];
            int bytesRead;
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                output.write(buffer, 0, bytesRead);
            }
            graphDef = output.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        }
        //Place the .pb file generated before in the assets folder and import it as a byte[] array.
        // Let the array's name be graphdef.
        //Now, load the graph from the graphdef:
        graph.importGraphDef(graphDef);
        try {
            //Now, load the checkpoint by running the restore checkpoint op in the graph:
            sess.runner().feed("save/Const", checkpointPrefix).addTarget("save/restore_all").run();
            Toast.makeText(this, "Checkpoint Found and Loaded!", Toast.LENGTH_SHORT).show();
        }
        catch (Exception e) {
            //Alternatively, initialize the graph by calling the init op:
            sess.runner().addTarget("init").run();
            Log.i("Checkpoint: ", "Graph Initialized");
        }
    }
    //**
    // (ii) Performing Inference using the model
    // FUNCION QUE USA EL MODLEO PARA OBTENER EL OUTPUT ?
    //**
    //feature en mi caso es num1 que es math.random
    private float predictPrueba(float features) {
        float n_epochs = num_epoch;
        float num1 = (float) Math.random();
        float output = 0; //y

        //First, create an input tensor:
        /*

         */

        Tensor input = Tensor.create(features);
        Tensor op_tensor = sess.runner().feed("input",input).fetch("output").run().get(0).expect(Float.class);
        //para escribir en la app en W y B test
        ArrayList<Tensor<?>> values = (ArrayList<Tensor<?>>) sess.runner().fetch("W/read").fetch("b/read").run();


        Wtest.setText("W_inicial: "+(Float.toString(values.get(0).floatValue())));
        Btest.setText("b_inicial: "+Float.toString(values.get(1).floatValue()));
        y_mejoras_w.add(((values.get(0).floatValue())));
        x_mejoras_w.add( ""+(0+ num_epoch*num));

        y_mejoras_b.add(((values.get(1).floatValue())));
        x_mejoras_b.add( ""+(0+ num_epoch*num));



        return output;
    }


    private float Funcionar_salida(float features) {
        float n_epochs = num_epoch;
        float num1 = (float) Math.random();
        float output = 0; //y


        Tensor input = Tensor.create(features);
        Tensor op_tensor = sess.runner().feed("input",input).fetch("output").run().get(0).expect(Float.class);
        //para escribir en la app en W y B test
        ArrayList<Tensor<?>> values = (ArrayList<Tensor<?>>) sess.runner().fetch("W/read").fetch("b/read").run();

        //CREAR UN TEXTO PARA ESCRIBIR EL OUTPUT PREDECIDO: Out

        Y.setText("Salida: Y= "+ Float.toString(op_tensor.floatValue()) +", si entrada X=1");



        return output;
    }





    //SI MODELO Y= M*X + C
    //EN INPUT= X_TRAIN SE PONE EL PARAMETRO DE ENTRADA, QUE ES X.(ver el otro ejemplo de regresion)
    //EN TARGET=Y_TRAIN, QUE ES EN ESTE CASO Y= M*X + C(ver ejemplo)
    //con session.runner.feed.... se usa el modelo.
    //private String trainPrueba(float features, float[] label, int epochs){
    private String trainPrueba(float features, int epochs){


        //First, create the tensors for the input and the labels:

        // Tensor y_train = Tensor.create(label);                  //output
        //Then, use the ‘train_op’ graph operation defined in the graph to train the graph:
        Random random = new Random();
        int ctr = 0;
        int h = epochs - 2;
        while (ctr < epochs) {
            float in = random.nextFloat();

            org.tensorflow.Tensor x_train = Tensor.create(in); //input
            Tensor y_train = Tensor.create(10*in + 2);         //output



            sess.runner().feed("input", x_train).feed("target", y_train).addTarget("train").run();

            ArrayList<Tensor<?>> values = (ArrayList<Tensor<?>>) sess.runner().fetch("W/read").fetch("b/read").run();
            W.setText("W_final: "+(Float.toString(values.get(0).floatValue())));
            B.setText("b_final: "+Float.toString(values.get(1).floatValue()));
            ctr++;

            if (ctr == h) {

                pesos.add(0,(Float.toString(values.get(0).floatValue())));
                Log.i("valor 0: ", pesos.get(0));
                pesos.add(1,(Float.toString(values.get(1).floatValue())));
                Log.i("valor 1: ", pesos.get(1));


            }
        }
        return "Model Trained";
    }

    private String trainPrueba900(float features, int epochs){



        org.tensorflow.Tensor x_train = Tensor.create(features); //input
        Tensor y_train = Tensor.create(10*features + 2);         //output
        // Tensor y_train = Tensor.create(label);                  //output
        //Then, use the ‘train_op’ graph operation defined in the graph to train the graph:
        int ctr = 0;
        while (ctr < epochs) {


            // sess.runner().feed("input", x_train).feed("target", y_train).addTarget("train_op").run();
            sess.runner().feed("input", x_train).feed("target", y_train).addTarget("train").run();

            ArrayList<Tensor<?>> values = (ArrayList<Tensor<?>>) sess.runner().fetch("W/read").fetch("b/read").run();
            W.setText((Float.toString(values.get(0).floatValue())));
            B.setText(Float.toString(values.get(1).floatValue()));
            ctr++;
        }
        return "Model Trained";
    }



    //**
    //C. Extracting weights from the on-device model
    //**
    public ArrayList<ArrayList<Tensor<?>>> getWeightsPrueba() {
        ArrayList<Tensor<?>> w1 = (ArrayList<Tensor<?>>) sess.runner().fetch("W").run();
        ArrayList<Tensor<?>> b1 = (ArrayList<Tensor<?>>) sess.runner().fetch("b").run();
        ArrayList<ArrayList<Tensor<?>>> ls = new ArrayList<>();
        ls.add(w1);
        ls.add(b1);
        //  Log.i("Shapes: ", w1.get(0).shape()[0] + ", " + w1.get(0).shape()[1]);   PROBLEMA: NO EXISTE W1.GET(0).SHAPE()[1]
        //  Log.i("Shapes: ", b1.get(0).shape()[0] + ", " + b1.get(0).shape()[1]);
        Log.i("Shapes: ", String.valueOf(w1.get(0).shape()));  //CON EL [0] FALLA PORQUE NO EXISTE ???
        Log.i("Shapes: ", String.valueOf(b1.get(0).shape()));
        Log.i("Valor: ", String.valueOf(b1.get(0)));
        return ls;
    }

    //////////////////////////////////////////////////////////////////////////////////
    public void writeFileLinear() {
        textFile = new File(getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), "/file1prueba");
        try{
            FileOutputStream fos = new FileOutputStream(textFile);
            String mensaje = "esto es un mensaje de prueba \n";
            String mensaje_final = mensaje + "\n" + pesos.get(0) + "\n" + pesos.get(1);
            Log.i("valor 0 final: ", pesos.get(0));
            Log.i("valor 1 final: ", pesos.get(1));
            fos.write(mensaje_final.getBytes());
            fos.close();
            file = textFile;
            Log.i("Error: FILE", "Fichero con msg creado!");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    //SE GUARDAN LOS WEIGHTS EN EL DISPOSITIVO

    public void finalSave1() {
        ArrayList<ArrayList<Tensor<?>>> at = getWeightsPrueba();
        int ctr = 0;
        ArrayList<float[]> diff = new ArrayList<>();
        ArrayList<ArrayList<Tensor<?>>> bt = getWeightsPrueba();
        for (int x = 0; x < 2; x++) {   ///vale 2 porque solo w1 y b1
            ArrayList<Tensor<?>> u1 = at.get(x); //para pruebas
            Tensor<?> u = at.get(x).get(0); //variable auxiliar para pruebas
            float[] d = new float[flattenedWeight(bt.get(x).get(0)).length];
            float[] bw = flattenedWeight(bt.get(x).get(0));
            float[] aw = flattenedWeight(at.get(x).get(0));

            diff.add(aw);

            // float aux = at.get(x).get(0);
            // diff.add(at.get(x).get(0));
            for(int j = 0; j < bw.length; j++)
            {
                d[j] = aw[j] - bw[j];
            }
            diff.add(d);
        }
        Log.i("COUNTER: ", String.valueOf(ctr));
        savePrueba1(diff);
    }
    public void finalSave_linear() {

        ArrayList<float[]> diff = new ArrayList<>();
        float [] h1 = new float[8];
        float [] h2 = new float[2];
        diff.add(h1);
        diff.add(h2);

        savePrueba1(diff);
    }
    public void savePrueba1MIO(ArrayList<float[]> diff){
        ArrayList<ArrayList<Tensor<?>>> at = getWeightsPrueba();
        float[] d1 = diff.get(0);
        float[] d2 = diff.get(1);

        int l1 = diff.get(0).length;
        int l2 = diff.get(1).length;

        int ctr = 0;
        int i = 0;
        int j = 0;
        float[] result = new float[l1 + l2 ];
        for(i = 0, j = 0; j < l1; i++, j++)
        {
            result[i] = d1[j];
        }
        for(int k = 0; k < l2; i++, k++)
        {
            result[i] = d2[k];
        }

        for(float x: result)
        {
            if(x == 0.0)
                ctr++;
        }
        Log.i("COUNTER_A: ", String.valueOf(ctr));
        Log.i("Result Length:  ", String.valueOf(ctr));

        saveWeightsPrueba1(result, "WeightsPrueba.bin");
    }
    public void savePrueba1(ArrayList<float[]> diff){

        float[] d1 = diff.get(0);
        float[] d2 = diff.get(1);

        int l1 = diff.get(0).length;
        int l2 = diff.get(1).length;

        int ctr = 0;
        int i = 0;
        int j = 0;
        float[] result = new float[l1 + l2 ];
        for(i = 0, j = 0; j < l1; i++, j++)
        {
            result[i] = d1[j];
        }
        for(int k = 0; k < l2; i++, k++)
        {
            result[i] = d2[k];
        }

        for(float x: result)
        {
            if(x == 0.0)
                ctr++;
        }
        Log.i("COUNTER_A: ", String.valueOf(ctr));
        Log.i("Result Length:  ", String.valueOf(ctr));

        saveWeightsPrueba1(result, "WeightsPrueba.bin");
    }
    public void saveWeightsPrueba1(float[] diff, String name) {
        byte[] byteArray = new byte[diff.length * 4]; // es cuatro pero no se por que
        // wrap the byte array to the byte buffer
        ByteBuffer byteBuf = ByteBuffer.wrap(byteArray);
        for(byte b: byteBuf.array())
        {
            Log.i("ByteBuffer: ", String.valueOf(b));

        }
        // create a view of the byte buffer as a float buffer
        FloatBuffer floatBuf = byteBuf.asFloatBuffer();


        // now put the float array to the float buffer,
        // it is actually stored to the byte array
        floatBuf.put(diff);
        saveFilePrueba1(byteArray, name);
    }
    public void saveFilePrueba1(byte[] byteArray, String name) {
        File file = new File(getApplicationContext().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), name);
        if (!file.exists()) {
            try {
                file.createNewFile();
            } catch (IOException e) {
                Log.i("Error: FILE", "File not Created!");
            }
        }
        OutputStream os = null;
        try {
            os = new FileOutputStream(file);
        } catch (FileNotFoundException e) {
            Log.i("Error: FILE", "File not found!");
        }
        try {
            os.write(byteArray);
            Log.i("FileWriter", "File written successfully");
        } catch (IOException e) {
            Log.i("Error: FILE", "File not written!");
        }
    }

    public void savePrueba(ArrayList<float[]> diff){


        int l1 = diff.get(0).length;
        int l2 = diff.get(1).length;


        float[] resultPrueba = new float[l1 + l2 ];
        System.arraycopy(diff.get(0), 0, resultPrueba, 0, l1);
        System.arraycopy(diff.get(1), 0, resultPrueba, l1, l2);


        saveWeightsPrueba(resultPrueba, "WeightsPrueba.bin");
    }

    public void saveWeightsPrueba(float[] diffPrueba, String name) {
        byte[] byteArray = new byte[diffPrueba.length * 2];  //multiplico por 2
        Log.i("Length of FloatArray: ", String.valueOf(diffPrueba.length));

        // wrap the byte array to the byte buffer
        ByteBuffer byteBuf = ByteBuffer.wrap(byteArray);

        // create a view of the byte buffer as a float buffer
        FloatBuffer floatBuf = byteBuf.asFloatBuffer();

        // now put the float array to the float buffer,
        // it is actually stored to the byte array
        floatBuf.put(diffPrueba);
        saveFilePrueba(byteArray, name);
    }

    public void saveFilePrueba(byte[] byteArray, String name) {
        File file = new File(getApplicationContext().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), name);
        if (!file.exists()) {
            try {
                file.createNewFile();
            } catch (IOException e) {
                Log.i("Error: FILE", "File not Created!");
            }
        }
        OutputStream os = null;
        try {
            os = new FileOutputStream(file);
        } catch (FileNotFoundException e) {
            Log.i("Error: FILE", "File not found!");
        }
        try {
            os.write(byteArray);
            Log.i("FileWriter", "File written successfully");
        } catch (IOException e) {
            Log.i("Error: FILE", "File not written!");
        }
    }

    public void writeFileTest() {
        textFile = new File(getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), "/file1prueba");
        try{
            FileOutputStream fos = new FileOutputStream(textFile);
            String mensaje = "esto es un mensaje de prueba";
            fos.write(mensaje.getBytes());
            fos.close();
            file = textFile;
            Log.i("Error: FILE", "Fichero con msg creado!");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    public void initializeGraph_check() {

        checkpointPrefix = Tensors.create((getApplicationContext().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS).getAbsolutePath() +  "/checkpoint_actualizado_"+modelctr+".ckpt").toString());
        modelctr++;
        checkpointDir = getApplicationContext().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS).getAbsolutePath();
        graph = new Graph();
        sess = new Session(graph);
        InputStream inputStream;
        try {
            inputStream = getAssets().open("graph5.pb");
            byte[] buffer = new byte[inputStream.available()];
            int bytesRead;
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                output.write(buffer, 0, bytesRead);
            }
            graphDef = output.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        }
        graph.importGraphDef(graphDef);
        try {
            sess.runner().feed("save/Const", checkpointPrefix).addTarget("save/restore_all").run();
            Toast.makeText(this, "Checkpoint Found and Loaded!", Toast.LENGTH_SHORT).show();
        }
        catch (Exception e) {
            sess.runner().addTarget("init").run();
            Log.i("Checkpoint: ", "Graph Initialized");
        }
    }


    public void Graficar_w () {
        List yAxisValues = new ArrayList();
        List axisValues = new ArrayList();


        Line line = new Line(yAxisValues).setColor(Color.parseColor("#9C27B0"));

        //    for (int i = 0; i < axisData.length; i++) {
        for (int i = 0; i < x_mejoras_w.size(); i++) {
            //   axisValues.add(i, new AxisValue(i).setLabel(axisData[i]));
            //    axisValues.add(i, x_mejoras_w.get(i));
            axisValues.add(i, new AxisValue(i).setLabel(x_mejoras_w.get(i)));

        }

        //  for (int i = 0; i < yAxisData.length; i++) {
        for (int i = 0; i < y_mejoras_w.size(); i++) {
            // yAxisValues.add(new PointValue(i, yAxisData[i]));
            yAxisValues.add(new PointValue(i, (float) y_mejoras_w.get(i)));
        }

        List lines = new ArrayList();
        lines.add(line);

        LineChartData data = new LineChartData();
        data.setLines(lines);

        Axis axis = new Axis();
        axis.setValues(axisValues);
        axis.setTextSize(16);
        axis.setName("Epocas");
        axis.setTextColor(Color.parseColor("#03A9F4"));
        data.setAxisXBottom(axis);

        Axis yAxis = new Axis();
        yAxis.setName("Valor W");
        yAxis.setTextColor(Color.parseColor("#03A9F4"));
        yAxis.setTextSize(16);
        data.setAxisYLeft(yAxis);

        lineChartView.setLineChartData(data);
        Viewport viewport = new Viewport(lineChartView.getMaximumViewport());
        //    viewport.top = 110;
        viewport.top = 10;
        lineChartView.setMaximumViewport(viewport);
        lineChartView.setCurrentViewport(viewport);
    }
    public void Graficar_b () {
        List yAxisValues = new ArrayList();
        List axisValues = new ArrayList();


        Line line = new Line(yAxisValues).setColor(Color.parseColor("#9C27B0"));

        //    for (int i = 0; i < axisData.length; i++) {
        for (int i = 0; i < x_mejoras_b.size(); i++) {
            //   axisValues.add(i, new AxisValue(i).setLabel(axisData[i]));
            //    axisValues.add(i, x_mejoras_w.get(i));
            axisValues.add(i, new AxisValue(i).setLabel(x_mejoras_b.get(i)));

        }

        //  for (int i = 0; i < yAxisData.length; i++) {
        for (int i = 0; i < y_mejoras_b.size(); i++) {
            // yAxisValues.add(new PointValue(i, yAxisData[i]));
            yAxisValues.add(new PointValue(i, (float) y_mejoras_b.get(i)));
        }

        List lines = new ArrayList();
        lines.add(line);

        LineChartData data = new LineChartData();
        data.setLines(lines);

        Axis axis = new Axis();
        axis.setValues(axisValues);
        axis.setTextSize(16);
        axis.setName("Epocas");
        axis.setTextColor(Color.parseColor("#03A9F4"));
        data.setAxisXBottom(axis);

        Axis yAxis = new Axis();
        yAxis.setName("Valor W");
        yAxis.setTextColor(Color.parseColor("#03A9F4"));
        yAxis.setTextSize(16);
        data.setAxisYLeft(yAxis);

        lineChartView2.setLineChartData(data);
        Viewport viewport = new Viewport(lineChartView2.getMaximumViewport());
        //    viewport.top = 110;
        viewport.top = 4;
        lineChartView2.setMaximumViewport(viewport);
        lineChartView2.setCurrentViewport(viewport);

    }


}

