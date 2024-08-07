package com.example.surfaceview;

public class FlashlightCone {
    private int mX;
    private int mY;
    private int mRadius;

    public FlashlightCone(int viewWidth, int viewHeight) {
        mX = viewWidth/2;
        mY = viewHeight/2;
        mRadius = ((viewWidth <= viewHeight) ? mX / 3 : mY / 3);
    }

    public int getmX() {
        return mX;
    }

    public int getmY() {
        return mY;
    }

    public int getmRadius() {
        return mRadius;
    }

    public void update(int newX, int newY) {
        mX = newX;
        mY = newY;
    }
}
