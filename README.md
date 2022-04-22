# cv-toolkit
Various random computer vision utility scripts, mostly Python or shell.

# Useful Bash Utilities

## Turn rgb into greyscale

```bash
# single version
magick mogrify -colorspace gray *.jpg

# parallel version
parallel -X magick mogrify -colorspace gray ::: *.jpg
```

## Find and count all images in a directory

```bash
find . -type f | sed -e 's/.*\.//' | sort | uniq -c | sort -n | grep -Ei '(tiff|bmp|jpeg|jpg|png|gif)$'
```
