def cudanize(hist, nbrs, fut, sc_img):
    """This script takes the network input tensors and creates the tensors on cuda.
    """
    hist = hist.cuda()
    nbrs = nbrs.cuda()
    fut = fut.cuda()
    sc_img = sc_img.cuda()

    return hist, nbrs, fut, sc_img
