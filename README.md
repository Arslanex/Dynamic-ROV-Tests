# Servo Kontrol Tetleri
Kodun temel işleyişi eğer aranan obje belirli bir piksel değerinden sağda ise arduinoya 'R' verisini, belirli bir piksel değerinden solda ise 'L' değerini göndererek servoyu yönlendirecektir. Servo da belirtilen yöne 10 derece dönerek yeni merkez noktası yapıp yeni verileri bekleyecektir. 

## Deneme 1 :
Standar tespit algoritmasının içine belirli bir oranda sağada veya solda kalması durumuna arduinoya servonun hangi yöne döneceğini belirten bir mesaj gönderttim. 

https://user-images.githubusercontent.com/44752389/176529839-1e5c434f-9e82-497a-9bfe-953593649e22.mp4


## Deneme 2 :
İlk testte aldığım FPS çok düşük olduğu için alternatif bir çözüme gitmem gerekti. Thread kullanarak kodun işleyişini hızlandırmayı denedim. Kameradan video verisini çekme, bunu kullanıcıya gösterme, tespit fonksiyonu ve seri haberleşmeyi bir thread'e atayarak daha hızlı bir kod haline çevirdim. Hala seri haberleşmeden dolayı bir gecikme olsada ilk denemeye göre FPS oldukça arttı.

https://user-images.githubusercontent.com/44752389/176470207-0c32175d-abe5-4693-aad7-853ac4863aeb.mp4

