[app]

# App info
title = PLAYTREE
package.name = playtree
package.domain = org.rhystech
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json
source.include_patterns = assets/*,src/*

# Version
version = 1.0.0

# Requirements
requirements = python3,pygame-ce,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.arch = arm64-v8a

# Back key
android.back_key = Back

# Orientation
orientation = landscape

# Icon
icon.filename = %(source.dir)s/../assets/icon.png
presplash.filename = %(source.dir)s/../assets/presplash.png

# Window
fullscreen = 1
android.window_soft_input_mode = adjustResize

# Build
android.release_artifact = apk
android.debug_artifact = apk

# Debug
log_level = 2
warn_on_root = 0

# iOS (not used but required)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_endpoint_release = 
ios.ios_deploy_endpoint_debug = 

# P4A
p4a.branch = develop
p4a.bootstrap = sdl2

# Presplash
#presplash.color = #102015
