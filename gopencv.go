package main

import (
	"bytes"
	"crypto/md5"
	"fmt"
	"github.com/hoisie/web"
	"io"

	"code.google.com/p/go-opencv/trunk/opencv"
)

var page = `
<html>
<head><title>Multipart Test</title></head>
<body>
<form action="/multipart" enctype="multipart/form-data" method="POST">

<label for="image"> Please select a File </label>
<input id="image" type="file" name="image"/>
<br>
<label for="image2"> Please select a File </label>
<input id="image2" type="file" name="image2"/>
<br>
<input type="submit" name="Submit" value="Submit"/>
</form>
</body>
</html>
`

func index() string { return page }

func multipart(ctx *web.Context) string {
	ctx.Request.ParseMultipartForm(10 * 1024 * 1024)
	form := ctx.Request.MultipartForm
	var output bytes.Buffer
	output.WriteString("<p>input1: " + form.Value["input1"][0] + "</p>")
	output.WriteString("<p>input2: " + form.Value["input2"][0] + "</p>")

	fileHeader := form.File["image"][0]
	filename := fileHeader.Filename
	image := opencv.LoadImage(filename)
	if image == nil {
		panic("LoadImage fail")
	}
	defer image.Release()

	output.WriteString("<p>image " + filename + " " + image + "</p>")
	return output.String()
}

func main() {
	web.Get("/", index)
	web.Post("/multipart", multipart)
	web.Run("0.0.0.0:9999")
}
