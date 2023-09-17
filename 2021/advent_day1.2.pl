use strict;
use warnings;
my @threes;
my $counter = 0;

open my $fh, "input.txt";
my @inputs = <$fh>;
close $fh;

my $done = 0;
while (not $done) {
    if ($counter + 2 < @inputs) {
      push @threes, $inputs[$counter]+$inputs[$counter]+$inputs[$counter+2];
    }
  $done = $counter > @inputs;
  $counter++;
}

my $last;
my $up;
while (my $line = shift @threes) {
  chomp $line;
  $last = $line unless defined $last;
  if ($line > $last) {
    $up++;
  }
  $last = $line;
}
print "$up\n";
