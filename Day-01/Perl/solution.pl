# the dial turns 
# left and right
# counting zeros
# fifty starts, mod a hundred
# R adds L, subtracts, zero increments
# answer from arithmetic dance
# magic obscures simple truth
$_=q[0123456789];$p=ord(substr$_,2,1);
$c=0;while(<>){/^([LR])(\d+)$/ or next;
$p=($p+($1eq"R"?$2:-$2))%100;
$c+=!$p}print"$c\n";
