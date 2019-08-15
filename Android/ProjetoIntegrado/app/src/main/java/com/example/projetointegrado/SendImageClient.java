package com.example.projetointegrado;

import android.os.AsyncTask;

import java.io.DataOutputStream;
import java.io.OutputStream;
import java.net.Socket;

public class SendImageClient extends AsyncTask<byte[], Void, Void> {
    @Override
    protected Void doInBackground(byte[]... bytes) {
        try{
            Socket socket = new Socket("Server IP", 8080);

            OutputStream outputStream = socket.getOutputStream();
            DataOutputStream dataOutputStream = new DataOutputStream(outputStream);
            dataOutputStream.write(bytes[0], 0, bytes[0].length);
            dataOutputStream.close();
            outputStream.close();
            socket.close();

        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }
}
