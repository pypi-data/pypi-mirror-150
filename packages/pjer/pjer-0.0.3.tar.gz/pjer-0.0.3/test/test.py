import pjer
model = [1,1,1,0
        ,0,1,1,1
        ,1,1,1,1
        ,1,0,1,0]

pjer.sprite(model,100).draw(10,0,10)
pjer.sprite(model,100).undraw(10,0,10)
pjer.sprite(model,100).draw(0,0,10)