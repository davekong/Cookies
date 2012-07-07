package main

import (
	"bytes"
	"strings"
	"fmt"
	"io"
	"os"
	"net/http"
	"encoding/xml"
)

// Write all of the CharData found to b until the EndElement with Local Name tag is reached.
func TxtTillTag(b *bytes.Buffer, tag string, d *xml.Decoder) error {
	for {
		toktxt, err := d.Token()
		if err != nil {
			return err
		}
		if txt, ok := toktxt.(xml.CharData); ok {
			b.Write(txt)
		} else if ee, ok := toktxt.(xml.EndElement); ok {
			if ee.Name.Local == tag {
				break
			}
		}
	}
	return nil
}

func main() {
	resp, err := http.Get(os.Args[1])
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	b := new(bytes.Buffer)
	d := xml.NewDecoder(resp.Body)
	for {
		tok, err := d.Token()
		if err != nil {
			if err != io.EOF {
				fmt.Println(err)
			}
			break
		}
		switch tok.(type) {
		case xml.StartElement:
			name := tok.(xml.StartElement).Name.Local
			switch name {
			case "li":
				err := TxtTillTag(b, "li", d)
				b.WriteString("\n")
				if err != nil {
					break
				}
			case "h2":
				b.WriteString("\n")
				l0 := b.Len()
				err := TxtTillTag(b, "h2", d)
				l1 := b.Len()
				if strings.Contains(b.String()[l0:l1], "Ingredients") {
					b.WriteString("\n\nUse this!!!\n\n")
				}
				b.WriteString("\n=========================\n\n")
				if err != nil {
					break
				}
			}
		}
	}
	fmt.Println(b.String())
}
