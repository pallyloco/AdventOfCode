#!/usr/bin/perl
use strict;
use warnings;

%dictionary = (3=>"three",1=>"one",4=>"four",2=>"two",4=>"four")
@numbers_in_order = sort ($a <=> $b) keys %dictionary
print(@numbers);