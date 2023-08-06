from celery import shared_task


@shared_task
def drifters_garbage_collection():
    # Archive EOL >4??? maybe six or something to be sure? holes,
    # Set Decayed >12h to EOL
    #
    pass
