from google.cloud import storage, firestore
from fastapi import FastAPI, status

from model import Photo


db = firestore.Client(project="genuine-space-349906")
app = FastAPI()
# main route


@app.get("/")
async def root():
    return {"message": "Hello World"}


# sign up function
@app.post("/signup")
async def signup():
    pass

# sign in function


@app.post("/signin")
async def signin():
    pass

# get user credential


@app.get("/user")
async def user():
    pass

# Photos Model


@app.get('/make_photo_edit')
async def make_photo_edit():

    # get the docs, in this example is the doc with id
    doc_ref = db.collection(u"photos").document("gpeGwKKB2siJWssDQGko")
    real_doc = doc_ref.get().to_dict()

    # send the data into google pubsub

    return {"success": "true", "data": real_doc}


@app.get("/upload_photo", status_code=status.HTTP_201_CREATED)
async def upload_photo():
    """ Upload photo to the gcp bucket """
    bucket_name = "photoalbumsppl"
    source_file_name = "test_img_aot.jpg"
    destination_blob_name = "photos/{}.jpg".format(source_file_name)

    # call client bucket gcp
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # add photo to bucket
    # blob.upload_from_filename(source_file_name)

    # res = "File {} uploaded to {}.".format(
    #     source_file_name, destination_blob_name)

    # testing data
    name = "test_img_aot"
    photo_url = "https://storage.googleapis.com/photoalbumsppl/photos/test_img_aot.jpg.jpg"

    new_photo = Photo(url=photo_url,
                      vote=0,
                      thumbnail_url=photo_url,
                      square_url=photo_url,
                      userid='23123123',
                      name=name)

    # add to firestore
    doc_ref = db.collection(u"photos").document()
    doc_ref.set({
        u"url": new_photo.url,
        u"vote": new_photo.vote,
        u"thumbnail_url": new_photo.thumbnail_url,
        u"square_url": new_photo.square_url,
        u"userid": new_photo.userid,
        u"name": new_photo.name,
    })

    return {"id": doc_ref.id, **new_photo.dict()}

# upvote photo route


@app.get("/upvote", status_code=status.HTTP_202_ACCEPTED)
async def upvote_photo():

    # get the id of the photo

    doc_ref = db.collection(u"photos").document("gpeGwKKB2siJWssDQGko")

    # add the upvoote of the photo
    res = doc_ref.update({"vote": firestore.Increment(1)})

    # return success
    return {
        "message": "upvote success",
        **res.dict()
    }

# view top 10 photo with the highest rating route in day


@app.get('/top_10_photo_day')
async def top_10_photo_day():
    return {"message": "Top 10 Photo Day"}

# view top 10 photo with the highest rating route in month


@app.get('/top_10_photo_month')
async def top_10_photo_month():
    return {"message": "Top 10 Photo Month"}

# view top 10 photo with the highest rating route weekly


@app.get('/top_10_photo_week')
async def top_10_photo_week():
    return {"message": "Top 10 Photo Week"}

# view all photos from original, thumbnail and 1:1 resultion:


@app.get('/all_photos', status_code=status.HTTP_200_OK)
async def all_photos():

    # get all photos

    result = db.collection(u"photos").get()
    pat_l = []
    for doc in result:
        pat_l.append({"id": doc.id, **doc.to_dict()})

    return {
        "status": "success",
        "data": pat_l}


# resize the photo with the single click
@app.get('photo_resize')
async def photo_resize():
    return {"message": "Photo Resize"}
