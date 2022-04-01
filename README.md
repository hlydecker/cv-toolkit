# cv-toolkit
Various random computer vision utility scripts, mostly Python or shell.

## Turn rgb into greyscale

```bash
# single version
magick mogrify -colorspace gray *.jpg

# parallel version
parallel -X magick mogrify -colorspace gray ::: *.jpg
```
