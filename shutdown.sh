#!/bin/bash
ps aux | grep algobroker | grep python3 | awk '{print $2}' | xargs kill
