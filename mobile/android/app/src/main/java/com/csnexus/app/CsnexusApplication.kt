package com.csnexus.app

import android.app.Application
import com.csnexus.app.core.di.AppContainer

class CsnexusApplication : Application() {
    val container: AppContainer by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
        AppContainer(this)
    }

    override fun onCreate() {
        super.onCreate()
    }
}
