#!/bin/sh
exec taskiq worker src._taskiq:broker
