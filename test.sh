for f in *.csv
do 
	STATE=$(echo $f | cut -d "_" -f 1)
	#echo $STATE
	
	awk -F"," 'BEGIN { OFS = "," } {$12= $STATE; print}' $f > $STATE.csv
done
