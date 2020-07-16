// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.7.0;

contract adder
{
    
    int     total;
    
    constructor() public
    {
        total =  100;
    }
    
    function add_to_total(int a) public returns (int)
    {
        total = total + a;
        return total;
    }
    
    function get_total() public view returns (int)
    {
        return total;
    }
    
}

