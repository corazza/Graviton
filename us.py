from uni import *
from body import *


def start (uni, init, run, end, dt):
    init(uni)
    
    while run(uni):
        uni.update(dt)
        
    end(uni)
