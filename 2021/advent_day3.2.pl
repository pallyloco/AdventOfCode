#!/usr/bin/perl
use strict;
use warnings;

my @final_bits;
open my $fh, "input_day3_1.txt";
my @tmp = <$fh>;
close $fh;
my $result = \@tmp;
my $count = 0;
while (scalar(@$result) > 1) {
  $result = filter($result,$count,1);
  $count++;
}
my $oxygen = convert_bits_decimal($result->[0]);

$result = \@tmp;
$count = 0;
while (scalar(@$result) > 1) {
  $result = filter($result,$count,0);
  $count++;
}
my $co2 = convert_bits_decimal($result->[0]);
print "$oxygen, $co2\n";
print $oxygen * $co2, "\n";

sub convert_bits_decimal {
  my $binary = shift;
  chomp $binary;
  my $number =  0;
  foreach my $bit (split "",$binary) {
    $number = $number << 1;
    $number = $number + $bit;
  }
  return $number;
}


sub filter {
  my $array = shift;
  my $i = shift;
  my $find_max = shift;

  my $len = @$array;
  my @result;
  my $count = 0;
  foreach my $item (@$array) {
    $count++ if substr($item,$i,1);
  }
  my $condition = (($count >= $len/2) == $find_max) ;

  foreach my $item (@$array) {
    if ($condition) {
      push @result,$item if substr($item,$i,1) == 1;
    }
    else {
      push @result,$item if substr($item,$i,1) == 0;
    }
  }
  return \@result;
}
