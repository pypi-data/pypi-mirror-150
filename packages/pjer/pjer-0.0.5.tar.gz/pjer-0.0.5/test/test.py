import pjer
import handydandy
model = [1,1,1,0
        ,0,1,1,1
        ,1,1,1,1
        ,1,0,1,0]

pjer.sprite(model,100).draw(0,100,10)
handydandy.userinput.pause()