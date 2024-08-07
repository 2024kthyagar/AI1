package com.example.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.View;

import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;

import java.util.ArrayList;

public class DrawView extends View {
    private Paint p = new Paint();
    int startRippleX=5, startRippleY=725;
    int dX=10, dY=10;
    int numAsteroids =10;
    ArrayList<RectF> objects = new ArrayList<>();
    MountainSprite mountainSprite = new MountainSprite();
    Bitmap asteroidBMP = BitmapFactory.decodeResource(getResources(), R.drawable.comet_meteorite_clipart);
    Bitmap reverseAsteroidBMP = BitmapFactory.decodeResource(getResources(), R.drawable.reverse_comet_meteorite_clipart);
    Bitmap upAsteroidBMP = BitmapFactory.decodeResource(getResources(), R.drawable.up_comet_meteorite_clipart);
    Bitmap upReverseAsteroidBMP = BitmapFactory.decodeResource(getResources(), R.drawable.up_reverse_comet_meteorite_clipart);
    Bitmap explosionBMP = BitmapFactory.decodeResource(getResources(), R.drawable.explosion);
    public DrawView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        Bitmap[] bitmaps = {asteroidBMP, reverseAsteroidBMP, upAsteroidBMP, upReverseAsteroidBMP};
        for(int i=0; i<numAsteroids; i++) {
            objects.add(new AsteroidSprite((float) (Math.random()*1000),
                    (float) (Math.random()*600),
                    (float) (Math.random()*10+70),
                    bitmaps, explosionBMP));
        }
        objects.add(mountainSprite);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
       p.setColor(Color.BLUE);
        canvas.drawRect(0,700,getWidth(),800, p);
        p.setColor(ContextCompat.getColor(getContext(), R.color.light_blue));
        canvas.drawRect(0, 0, getWidth(),600,p);

        p.setColor(Color.GREEN);
        canvas.drawRect(0,800,getWidth(), getHeight(), p);
        canvas.drawRect(0, 600, getWidth(), 700, p);

        for (int i=0; i<objects.size(); i++) {
            RectF object = objects.get(i);
            if (object instanceof AsteroidSprite) {
                AsteroidSprite asteroid = (AsteroidSprite) object;
                asteroid.update(objects, i, getWidth(), getHeight());
                asteroid.draw(canvas);
            }
        }
        mountainSprite.draw(canvas);


        drawCloud(canvas, 700, 200, 105, 20);
        drawCloud(canvas, 600, 400, 75, 25);
        drawCloud(canvas, 550, 150, 75, 23);
        drawCloud(canvas, 725, 325, 75, 35);
        invalidate();

    }



    private void drawCloud(Canvas canvas, int x, int y, int width, int bubble) {
        Path cloudPath = new Path();
        cloudPath.moveTo(x, y);
        for(int i=0; i<width; i+=15) {
            if(i/15%2==0)
              cloudPath.addCircle(x+i, y+10, bubble, Path.Direction.CW);
            else
                cloudPath.addCircle(x+i, y-10, bubble, Path.Direction.CW);
        }

        Paint cloudPaint = new Paint();
        cloudPaint.setColor(Color.WHITE);
        canvas.drawPath(cloudPath, cloudPaint);

    }

}
