#!/usr/bin/ruby
class EjemploHilos
  require 'thread'
  def initialize
    @x = 0
    @estado = 0
    @orden = { :f1 => 1, :f2 => 0, :run => 2 }
    @mut = Mutex.new
    @cv = ConditionVariable.new
  end

  def run
    @estado = 0
    t1 = Thread.new {f1}
    t2 = Thread.new {f2}
    sleep 0.1
    @mut.lock
    @cv.wait(@mut) while (@estado != @orden[:run])
    puts '%d ' % @x
    @mut.unlock
  end

  def f1
    sleep 0.1
    @mut.lock
    @cv.wait(@mut) while (@estado != @orden[:f1])
    @x += 3
    @estado += 1
    @cv.broadcast
    @mut.unlock
  end

  def f2
    sleep 0.1
    @mut.lock
    @cv.wait(@mut) while (@estado != @orden[:f2])
    @x *= 2
    @estado += 1
    @cv.broadcast
    @mut.unlock
  end
end

e = EjemploHilos.new;10.times{e.run}
