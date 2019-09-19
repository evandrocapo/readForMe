package com.example.projetointegrado;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import android.app.Dialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.ColorMatrix;
import android.graphics.ColorMatrixColorFilter;
import android.graphics.Matrix;
import android.media.Image;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.ImageView;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

    private static final int CODE_CAMERA = 100;
    private String pictureImagePath = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        openBackCamera();
    }

    private void openBackCamera(){
        String timeStamp = fileName();
        File file = saveImageFile(timeStamp);

            Log.d("OpenCamera: ", "Successful to open the camera");
            Uri outputFileUri = FileProvider.getUriForFile(this, "com.example.projetointegrado", file);
            Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, outputFileUri);
            startActivityForResult(cameraIntent, CODE_CAMERA);

        //Log.e("OpenCamera: ", "(ERROR) Impossible to open the camera");
    }

    private String fileName(){
        return new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
    }

    private File saveImageFile(String timeStamp){
        String imageFileName = timeStamp + ".jpg";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        if(storageDir != null){
            Log.d("FileDir: ", "Successful to open this directory ( " + storageDir.getAbsolutePath() + " )");
            pictureImagePath = storageDir.getAbsolutePath() + "/" + imageFileName;
            return new File(pictureImagePath);
        }
        Log.e("FileDir: ", "(ERROR) Impossible to open this directory");
        return null;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(resultCode == RESULT_OK && requestCode == CODE_CAMERA){
            File imgFile = new File(pictureImagePath);
            if(imgFile.exists()){
                // Configure the image
                Matrix matrix = new Matrix();
                Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
                matrix.postRotate(90);
                ImageView myImage = (ImageView) findViewById(R.id.image1);
                myImage.setImageBitmap(Bitmap.createBitmap(myBitmap, 0, 0, myBitmap.getWidth(), myBitmap.getHeight(),
                        matrix, true));

                // Converting the bitmap to array of bytes
                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                Bitmap.createBitmap(myBitmap, 0,0, myBitmap.getWidth(), myBitmap.getHeight(), matrix, true).
                        compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
                byte[] arrayImage = byteArrayOutputStream.toByteArray();

                // Call the async method to execute the connection with sever
//                SendImageClient sendImageClient = new SendImageClient();
//                sendImageClient.execute(arrayImage);

                if(imgFile.delete()){
                    Log.d("DeleteImage: ", "Successful");
                }else{
                    Log.e("DeleteImage: ", "Failed");
                }
            }
        }
    }
}
