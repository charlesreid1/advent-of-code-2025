$_=q[0123456789];$p=ord(substr$_,2,1);$c=0;while(<>){/^([LR])(\d+)$/ or next;
$p=($p+($1eq"R"?$2:-$2))%100;$c+=!$p}print"$c\n";#---------------------------
#The dial turns left/right,counting zeroes.Fifty starts,modulo hundred.####
#R adds,L subtracts,zero increments.Answer from arithmetic dance.Perl#####
#magic obscures simple truth.--------------------------------------------#