package com.example.myapplication;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;

public class MountainSprite extends RectF {
    public MountainSprite(float left, float top, float right, float bottom) {
        super(left, top, right, bottom);
    }
    public MountainSprite() {
        this(100, 1100, 450, 1500);
    }

    public void draw(Canvas canvas) {
        drawMountain(canvas, (int) (this.left+150), (int) (this.top+50), 150, 250);
        drawMountain(canvas, (int) (this.left+250), (int) this.top, 100, 225);
        drawMountain(canvas, (int) (this.left+200), (int) (this.top+100), 100, 200);
        drawMountain(canvas, (int) (this.left+250), (int) (this.top+150), 75, 150);
        drawMountain(canvas, (int) (this.left+200), (int) (this.top+200), 100, 150);
        drawMountain(canvas, (int) (this.left+100), (int) (this.top+200), 75, 200);
    }

    private void drawMountain(Canvas canvas, int topX, int topY, int base, int height) {
        Path mountainPath = new Path();
        mountainPath.moveTo(topX, topY);
        mountainPath.lineTo(topX-base,topY+height);
        mountainPath.lineTo(topX+base, topY+height);
        mountainPath.close();

        Path snowPath = new Path();
        snowPath.moveTo(topX, topY);
        snowPath.lineTo(topX-base/3,topY+height/3);
        snowPath.lineTo(topX+base/3, topY+height/3);
        snowPath.close();

        Paint mountainPaint = new Paint();
        mountainPaint.setColor(Color.GRAY);
        canvas.drawPath(mountainPath, mountainPaint);

        Paint borderPaint = new Paint();
        borderPaint.setStyle(Paint.Style.STROKE);
        borderPaint.setStrokeWidth(3);
        canvas.drawPath(mountainPath, borderPaint);

        Paint snowPaint = new Paint();
        snowPaint.setColor(Color.WHITE);
        canvas.drawPath(snowPath, snowPaint);
    }
}
