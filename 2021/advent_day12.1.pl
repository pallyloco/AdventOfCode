#!/usr/bin/perl
use strict;
use warnings;

package Node;

sub new {
    my $class = shift;
    my $name  = shift;
    my $small = 0;
    my $start = 0;
    my $end = 0;
    if (lc($name) eq $name) {$small = 1;}
    $start = 1 if $name eq "start"; 
    $end = 1 if $name eq "end"; 
    my $self = {
                 -name              => $name,
                 -nodes             => {},
                 -size              => $small,
                 -visited           => {},
                 -num_times_visited => 0,
                 -start => $start,
                 -end => $end,
    };
    return bless $self;
}
sub nodes {
    my $self = shift;
    return $self->{-nodes};
}
sub is_start {
    my $self = shift;
    return $self->{-start};
}

sub is_end {
    my $self = shift;
    return $self->{-end};
}

sub is_small {
    my $self = shift;
    return $self->{-size};
}
sub name {
    my $self = shift;
    return $self->{-name};
}
sub add_node {
    my $self = shift;
    my $node = shift;
    $self->{-nodes}{$node->name} = $node;
}
    

package MAIN;
my %map;
open my $fh, "input_day12.txt" or die;

while ( my $line = <$fh> ) {
    chomp $line;
    my @nodes = split ("-",$line);
    foreach my $i (0..scalar(@nodes)-1) {
        $map{$nodes[$i]} = new Node($nodes[$i]) unless defined $map{$nodes[$i]};
    }
    foreach my $i (0..scalar(@nodes)-2) {
        $map{$nodes[$i]}->add_node($map{$nodes[$i+1]});
        $map{$nodes[$i+1]}->add_node($map{$nodes[$i]});
    }

}
my $paths = find_paths(\%map);
my $hash = {};
foreach my $path (@$paths) {
    $hash->{$path}++;
}
print scalar(keys %$hash),"\n";


sub find_paths {
    my $map =shift;
    my $start = $map->{'start'};
    my @paths;
    my $all_paths = recursive_find_path($map,$start,\@paths); 
    use Data::Dumper;print Dumper \@paths;   
    return \@paths;
}

sub recursive_find_path {
    my $map = shift;
    my $start = shift;
    my $paths = shift;
    my $current_path = shift || $start->name;
    
    foreach my $node (values %{$start->nodes}) {
        my $name = $node->name;
        next if ($node->is_start());
        my @small_caves = ($current_path =~ /([a-z]+)/g);
        my %visited;
        my $double = 0;
        foreach my $cave (@small_caves) {
            $visited{$cave}++;
            $double = 1 if ($visited{$cave} > 1)
        }
        
        next if ($node->is_small() && $current_path =~ /$name/ && $double);

        
        if ($node->is_end) {
            push @$paths,$current_path . "," . $name;
            next;
        }
        recursive_find_path($map,$node,$paths,$current_path. "," . $name);
    }
    
    
}



__DATA__
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
