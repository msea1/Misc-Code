# if needed
sudo sed -i "s/rights\=\"none\" pattern\=\"PDF\"/rights\=\"read\|write\" pattern\=\"PDF\"/" /etc/ImageMagick-6/policy.xml

# in folder with PDFs
for a in *.pdf; do convert -density 300 -depth 8 -quality 95 -trim "$a" "$(basename "${a%.*}").jpeg"; done
