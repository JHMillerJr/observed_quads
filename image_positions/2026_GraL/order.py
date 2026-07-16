import math
import numpy as np

# law of cosines
def lawCos(a,b,c):
    val = (a**2 + b**2 - c**2) / (2*a*b)
    agl = math.acos(np.clip(val, -1.0, 1.0)) * (180/(np.pi))
    return agl

#> returns images in arrival time order (inverse + quad theory)
def arrivalOrder(images, x0=0.0, y0=0.0):
    
    #> collecting distances
    oims = abs(np.linalg.norm(images - np.full(shape=images.shape, fill_value=[x0, y0]), axis=1)) # getting distances
    o_angles = np.arctan2(images[:,1], images[:,0])
    oims = np.hstack((np.array([oims]).T, np.array([o_angles]).T, images))

    #> sorts by distance
    oims = oims[oims[:,0].argsort()][::-1]
    
    #> if quad
    ordered = np.zeros(oims.shape)
    if len(oims) >= 4:
        
        #> finding max distance between ims 12 and 34
        ind = np.argmax([oims[0][0] - oims[1][0], oims[2][0] - oims[3][0]]) * 3 # either 0 or 3
        ordered[ind] = oims[ind] # adds 1st (or 4th) image to final array
        
        #> dropping 5th (not important)
        if len(oims) == 5:
            dummy = oims[:-1]
        else:
            dummy = oims
        
        #> finding opposite image
        dummy = dummy[dummy[:,1].argsort()]             # sorting by angle
        index = np.where(dummy[:,0] == oims[ind][0])[0] # finding chosen image
        dummy = np.roll(dummy, shift=-index, axis=0)    # rolling to make 1st (or 4th) image the 1st element
        
        #> assigning opposite
        if ind == 0: ordered[1] = dummy[2]
        else: ordered[2] = dummy[2]
        
        #> finding law of cosines angle between remaining images (other angle does not work for this!!)
        angle21 = lawCos(a=dummy[2][0], b=dummy[1][0], c=np.linalg.norm(dummy[2][2:]-dummy[1][2:]))
        angle23 = lawCos(a=dummy[2][0], b=dummy[3][0], c=np.linalg.norm(dummy[2][2:]-dummy[3][2:]))

        #> assigning remaining images
        if ind == 0: # if found 1st & 2nd
            if angle21 < angle23:
                ordered[2] = dummy[1] # image 3
                ordered[3] = dummy[3] # image 4
            else:
                ordered[2] = dummy[3] # image 3
                ordered[3] = dummy[1] # image 4
        else: # if found 4th & 3rd
            if angle21 < angle23:
                ordered[1] = dummy[1] # image 2
                ordered[0] = dummy[3] # image 1
            else:
                ordered[1] = dummy[3] # image 2
                ordered[0] = dummy[1] # image 1
        if len(oims) == 5:
            ordered[-1] = oims[-1] # filling in 5th image

        return ordered[:,2:] # quad
    
    return oims[:,2:] # if not quad


def plot(name, images):
    
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator, NullFormatter
    import matplotlib.pyplot as plt
    fontsize=12

    fig, ax = plt.subplots(1,1,figsize=(4,4))
    ax.set_xlabel(r'$\mathbf{\Delta RA}$', fontsize=fontsize, labelpad=5)
    ax.set_ylabel(r'$\mathbf{\Delta DEC}$', fontsize=fontsize)
    ax.set_title(f'{name}', fontsize=fontsize, fontweight='bold')
    ax.set_box_aspect(1)

    for i, im in enumerate(images):
        ax.scatter(im[0], im[1], marker=f'${i+1}$')
        ax.scatter(0, 0, marker='+', c='k')
        # ax.scatter(r, d, c='k', marker='.')
    # ax.scatter(0,0,marker='X', c='k')
    
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    m = max(abs(xlim[0]), abs(xlim[1]),
            abs(ylim[0]), abs(ylim[1]))
    
    ax.set_xlim(-m, m)
    ax.set_ylim(-m, m)

    ax.xaxis.set_inverted(True) 
    
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))

    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())

    ax.grid(ls=':', alpha=0.5, which='both')

    # plt.savefig(f'./figs/{name}.png', bbox_inches='tight', dpi=100)
    plt.show()


""" #> MAIN ==========================
================================== """

#> main function
if __name__ == '__main__':
    
    #> name
    import os
    print('> '+os.path.basename(__file__))
    
    #> B1555+375
    name = 'SDSS1138+0314'
    images = np.array([[ 0.75877816, -0.662     ],
                         [ 0.64296448,  0.326     ],
                         [-0.52715103,  0.114     ],
                         [ 0.06289872, -0.728     ]])
    
    ordered = arrivalOrder(images)
    print(ordered)
    plot(name, ordered)
    
    # end
# thank