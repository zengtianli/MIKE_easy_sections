for file in *.py; do
    sed -i '' "1s/^/# $file\n/" "$file"
done

