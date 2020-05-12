proper check for tbb install
diff --git a/setup.py b/setup.py
index d9af18611..418bcd3ab 100644
--- a/setup.py
+++ b/setup.py
@@ -182,11 +182,6 @@ def get_ext_modules():
                     found = p  # the latest is used
         return found

-    # Search for Intel TBB, first check env var TBBROOT then conda locations
-    tbb_root = os.getenv('TBBROOT')
-    if not tbb_root:
-        tbb_root = check_file_at_path(['include', 'tbb', 'tbb.h'])
-
     # Set various flags for use in TBB and openmp. On OSX, also find OpenMP!
     have_openmp = True
     if sys.platform.startswith('win'):
@@ -213,30 +208,39 @@ def get_ext_modules():
         else:
             omplinkflags = ['-fopenmp']

-    if tbb_root:
-        print("Using Intel TBB from:", tbb_root)
-        ext_np_ufunc_tbb_backend = Extension(
-            name='numba.np.ufunc.tbbpool',
-            sources=[
-                'numba/np/ufunc/tbbpool.cpp',
-                'numba/np/ufunc/gufunc_scheduler.cpp',
-            ],
-            depends=['numba/np/ufunc/workqueue.h'],
-            include_dirs=[os.path.join(tbb_root, 'include')],
-            extra_compile_args=cpp11flags,
-            libraries=['tbb'],  # TODO: if --debug or -g, use 'tbb_debug'
-            library_dirs=[
-                # for Linux
-                os.path.join(tbb_root, 'lib', 'intel64', 'gcc4.4'),
-                # for MacOS
-                os.path.join(tbb_root, 'lib'),
-                # for Windows
-                os.path.join(tbb_root, 'lib', 'intel64', 'vc_mt'),
-            ],
-        )
-        ext_np_ufunc_backends.append(ext_np_ufunc_tbb_backend)
+    # Disable tbb if forced by user with NUMBA_NO_OPENMP=1
+    if os.getenv("NUMBA_NO_TBB"):
+        print("TBB disabled")
     else:
-        print("TBB not found")
+        # Search for Intel TBB, first check env var TBBROOT then conda locations
+        tbb_root = os.getenv('TBBROOT')
+        if not tbb_root:
+            tbb_root = check_file_at_path(['include', 'tbb', 'tbb.h'])
+
+        if tbb_root:
+            print("Using Intel TBB from:", tbb_root)
+            ext_np_ufunc_tbb_backend = Extension(
+                name='numba.np.ufunc.tbbpool',
+                sources=[
+                    'numba/np/ufunc/tbbpool.cpp',
+                    'numba/np/ufunc/gufunc_scheduler.cpp',
+                ],
+                depends=['numba/np/ufunc/workqueue.h'],
+                include_dirs=[os.path.join(tbb_root, 'include')],
+                extra_compile_args=cpp11flags,
+                libraries=['tbb'],  # TODO: if --debug or -g, use 'tbb_debug'
+                library_dirs=[
+                    # for Linux
+                    os.path.join(tbb_root, 'lib', 'intel64', 'gcc4.4'),
+                    # for MacOS
+                    os.path.join(tbb_root, 'lib'),
+                    # for Windows
+                    os.path.join(tbb_root, 'lib', 'intel64', 'vc_mt'),
+                ],
+            )
+            ext_np_ufunc_backends.append(ext_np_ufunc_tbb_backend)
+        else:
+            print("TBB not found")

     # Disable OpenMP if we are building a wheel or
     # forced by user with NUMBA_NO_OPENMP=1
