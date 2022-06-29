# Dynamic-ROV-Tests 
Jetson Nano'da daha iyi FPS alabilmek için CUDA yani GPU kullanımını sağlamalıyız. Bunun için CUDA uyumlu OpenCV kurulumu gerekmektedir. Ben aşağıda belirttiğim link üzerinden indirme işlemini gerçekleştirdim.

Link :: https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html

Opencv kurulumu bittikten sonra kartın özelliklerini test etmek kaldı. Bunun için kendi yazdığım yazılımı kullanacağım. Basitçe özetlemem gerekir ise yazılımın üç ana gmrevi var :
1. OpenCV kurulumunu kontrol etme
2. CPU ve GPU gücünü karşılaştırma
3. FPS tesletleri yaparak tahmini FPS değerini öğrenme

Bunu kullanmak için repo içindeki __main__.py ve __CudaControl.py__ kod dosyaları gerekmektedir. Aynı dizine yerleştridikten sonra tek yapmanız gereken terminalden __main__.py dosyasını çalıştrımaktır. Geri kalanı uygulama menüsü üzerinden gerçekleştirebilirsiniz. Yazılımın full halinin linkinide aşağıda bulabilirsiniz.

System Check Yazılımı :: https://github.com/Arslanex/System-Check

Eğer OpenCV kurulumu doğru yapılmış ise geri kalan denemelri yapmaya devam edebilirsiniz. İlk olarak normal FPS değerini test etmek ile işleme başladım. Sonrasonda Yolov3-320, Yolov3-416 ve Yolov3-Tiny modellerini kullanarak FPS tesleri yaptım. Aldığım sonuçlar aşağıdaki gibi oldu.

- Normal ::
- Yolov3-320 ::
- Yolov3-416 ::
- Yolov3-Tiny ::
