# TimelapseLiveView
A very simple "live view" for images generated for a timelapse. It accepts images pushed with a secret over HTTP and shows them with a configurable update rate.

## Configuration
Create a `.env` file and set a random `UPLOAD_KEY=` as well as the `PUBLISH_PORT=` variable. Use this key to upload the images to the server. 

### Cropping
By default the complete image is shown. To cut away parts of a camera image, set an environment variable (e.g. in the `.env` file) per camera:

```
CROP_<CAMERA>=x1,y1,x2,y2
```

`<CAMERA>` is the uploaded file name without extension, in upper case, with every character other than `A-Z` and `0-9` replaced by `_` (so `front-door.jpg` becomes `CROP_FRONT_DOOR`). `x1,y1` and `x2,y2` are two opposite corners, in pixels, of the area to keep. Coordinates start at `0,0` in the top left corner. The image is cropped when it's uploaded, so the removed part is never stored on the server. Changes take effect with the next upload.

## favicon.svg aka Video_Camera_Icon.svg
The `favicon.png` is copied from [wikimedia commons](https://commons.wikimedia.org/wiki/File:Video_Camera_Icon.svg).
