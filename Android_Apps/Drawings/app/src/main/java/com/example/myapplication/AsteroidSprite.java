package com.example.myapplication;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;

import java.util.ArrayList;

public class AsteroidSprite extends RectF {
    int dX, dY;
    float rad;
    int color;
    private Bitmap[] bitmap;
    private Bitmap explosion;
    public AsteroidSprite(float left, float top, float right, float bottom, float rad, int dX, int dY, Bitmap[] bitmap, Bitmap explosion) {
        super(left, top, right, bottom);
        this.rad=rad;
        this.dX =dX;
        this.dY = dY;
        this.bitmap = bitmap;
        this.explosion = explosion;
    }

    public AsteroidSprite(float left, float top, float right, float bottom, float rad, Bitmap[] bitmap, Bitmap explosion) {
        this(left, top, right, bottom, rad, (int) (Math.random()*80+20), (int) (Math.random()*20+20), bitmap, explosion);
    }

    public AsteroidSprite(float rad, int dX, int dY, Bitmap[] bitmap, Bitmap explosion) {
        this(1f,1f,rad, rad*2+1,rad*2+1,dX,dY, bitmap, explosion);
    }

    public AsteroidSprite(float left, float top, float size, Bitmap[] bitmap, Bitmap explosion) {
        this(left, top, left+size*2, top+size*2, size, bitmap, explosion);
    }


    public void update(ArrayList<RectF> list, int index, int width, int height) {
        offset(dX, dY);
        for (int i=index; i<list.size(); i++) {
            RectF r = list.get(i);
            if(r!=this) {
                if ((this.bottom>=r.top || this.top<=r.bottom) && RectF.intersects(this, r)) {
//                    System.out.println("I INTERSECTED WITH " + r);
                    this.dY *= -1;

                }
                if ((this.right>=r.left || this.left<=r.right) && RectF.intersects(this, r)) {
//                    System.out.println("I INTERSECTED WITH " + r);
                    this.dX *= -1;
                }
            }
        }
        if(this.top<=0 || this.bottom>=height)
            this.dY*=-1;
        if(this.left<=0 || this.right>=width)
            this.dX*=-1;
    }

    public void draw(Canvas canvas) {
        if(dX<0 && dY>0)
            canvas.drawBitmap(bitmap[0], null, this, null);
        else if(dX>0 && dY>0)
            canvas.drawBitmap(bitmap[1], null, this, null);
        else if(dX<0 && dY<0)
            canvas.drawBitmap(bitmap[2], null, this, null);
        else
            canvas.drawBitmap(bitmap[3], null, this, null);

    }

    public String toString() {
        return String.format("Center: (%1$f, %2$f) with radius %3$f", this.centerX(), this.centerY(), rad);
    }

}
