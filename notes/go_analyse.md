- [源码解析Github](#源码解析github)
- [Slice 解析](#slice-解析)
- [Map 解析](#map-解析)
- [Atomic原子操作](#atomic原子操作)
- [sync.Map详解](#syncmap详解)
- [Sync.Once](#synconce)

# 源码解析Github

[源码解析Github](https://github.com/DasyDong/GoExpertProgramming)  

# Slice 解析

源码 go\src\runtime\slice.go


```
type slice struct {
   array unsafe.Pointer
   len   int
   cap   int
}
```
```
func makeslice(et *_type, len, cap int) slice {
   p := mallocgc(et.size*uintptr(cap), et, true)
   return slice{p, len, cap}
}
```

根据容量cap*元素size，申请一块内存。mallocgc大空间（大于32kb）才会在heap堆上申请，否则在栈上分配，具体以后再介绍。

这里我们就看到切片底层就是数组，特别的是切片可以增长。

**关于增长grow**
```
// it returns a new slice with at least that capacity, with the old data
// copied into it.
// The new slice's length is set to the old slice's length,
// NOT to the new requested capacity.
// This is for codegen convenience. The old slice's length is used immediately
// to calculate where to write new values during an append.
```

```
方法返回的新切片容量至少达到请求，也就是说新的容量可能比申请的多；
copy老数据，也就是说有性能损耗；
len一致，因为数据内容不变.
```

**关于CAP**

```
 newcap := old.cap
   doublecap := newcap + newcap
   if cap > doublecap {
      newcap = cap
   } else {
      if old.len < 1024 {
         newcap = doublecap
      } else {
         for newcap < cap {
            newcap += newcap / 4
         }
      }
   }
```

cap增长策略：

* 如果期望大于double，新cap就等于期望；
* 如果当前大小小于1024，则两倍增长；
* 否则每次增长25%，直到满足期望。

# Map 解析

源码 go\src\runtime\hashmap.go

**简介**

```
// A map is just a hash table. The data is arranged
// into an array of buckets. Each bucket contains up to
// 8 key/value pairs. The low-order bits of the hash are
// used to select a bucket. Each bucket contains a few
// high-order bits of each hash to distinguish the entries
// within a single bucket.
//
// If more than 8 keys hash to a bucket, we chain on
// extra buckets.
//
// When the hashtable grows, we allocate a new array
// of buckets twice as big. Buckets are incrementally
// copied from the old bucket array to the new bucket array.
//
// Map iterators walk through the array of buckets and
// return the keys in walk order (bucket #, then overflow
// chain order, then bucket index).  To maintain iteration
// semantics, we never move keys within their bucket (if
// we did, keys might be returned 0 or 2 times).  When
// growing the table, iterators remain iterating through the
// old table and must check the new table if the bucket
// they are iterating through has been moved ("evacuated")
// to the new table.
```

map就是一个hash表。数据被分配到bucket桶数组中。每个桶有8个kv键值对。hash值的低八位用来选择桶。高八位用来在桶内部区分kv。这个很有意思，因为一个指针就是8位。

如果桶中kv超过8个，就新建一个桶，与之相连。

当hash表需要扩容时，我们每次增长两倍的桶数组。桶会从老的桶数组赋值到新的桶数组。

为了维护迭代语义，我们不会移动桶中的key（如果这么做了，key有可能返回0次或者2次）。扩容时，迭代器迭代老表，并且必须检查新表，是否正在迭代的桶已经撤离到了新表。

**struct**

```
type hmap struct {
   count     int // # live cells == size of map.  Must be first (used by len() builtin)
   flags     uint8
   B         uint8  // log_2 of # of buckets (can hold up to loadFactor * 2^B items)
   noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
   hash0     uint32 // hash seed

   buckets    unsafe.Pointer // array of 2^B Buckets. may be nil if count==0.
   oldbuckets unsafe.Pointer // previous bucket array of half the size, non-nil only when growing
   nevacuate  uintptr        // progress counter for evacuation (buckets less than this have been evacuated)
   overflow *[2]*[]*bmap
}
```

重要属性：

* buckets，桶数组，长度2^B
* oldbuckets，老桶数组，扩容时不为nil
* nevacuate，num evacuate，撤离进度，小于它的都已经撤离到新桶数组
* overflow *[2]*[]*bmap，这个挺有意思的，长度为2的数组，元素是桶数组。overflow 保存溢出的桶，即桶超过8个kv。overflow[0]对应buckets溢出，overflow[1]对应oldbuckets溢出。

```
// A bucket for a Go map.
type bmap struct {
   // tophash generally contains the top byte of the hash value
   // for each key in this bucket. If tophash[0] < minTopHash,
   // tophash[0] is a bucket evacuation state instead.
   tophash [bucketCnt]uint8
}
```

桶中只有一个8字节数组，长度为8。tophash保存hash的高8位，根据高8位找到条目。value保存这里就跟大多数map实现不一样，揣测8位就是value的指针？

**创建**

```
func makemap(t *maptype, hint int64, h *hmap, bucket unsafe.Pointer) *hmap {
   // find size parameter which will hold the requested # of elements
   B := uint8(0)
   for ; overLoadFactor(hint, B); B++ {
   }

   buckets := bucket
   if B != 0 {
      buckets = newarray(t.bucket, 1<<B)
   }

   // initialize Hmap
   if h == nil {
      h = (*hmap)(newobject(t.hmap))
   }
   h.count = 0
   h.B = B
   h.flags = 0
   h.hash0 = fastrand()
   h.buckets = buckets
   h.oldbuckets = nil
   h.nevacuate = 0
   h.noverflow = 0

   return h
}
```

根据B，创建长度2^B的桶数组。这里B会受到初始值8和load factor平衡因子的影响。

**访问**
```
func mapaccess2(t *maptype, h *hmap, key unsafe.Pointer) (unsafe.Pointer, bool) {
   alg := t.key.alg
   hash := alg.hash(key, uintptr(h.hash0))
   m := bucketMask(h.B)
   b := (*bmap)(unsafe.Pointer(uintptr(h.buckets) + (hash&m)*uintptr(t.bucketsize)))
   if c := h.oldbuckets; c != nil {
      oldb := (*bmap)(unsafe.Pointer(uintptr(c) + (hash&m)*uintptr(t.bucketsize)))
      if !evacuated(oldb) {
         b = oldb
      }
   }
   top := tophash(hash)
   for ; b != nil; b = b.overflow(t) {
      for i := uintptr(0); i < bucketCnt; i++ {
         if b.tophash[i] != top {
            continue
         }
         k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
         if t.indirectkey {
            k = *((*unsafe.Pointer)(k))
         }
         if alg.equal(key, k) {
            v := add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.valuesize))
            if t.indirectvalue {
               v = *((*unsafe.Pointer)(v))
            }
            return v, true
         }
      }
   }
   return unsafe.Pointer(&zeroVal[0]), false
}
```

* 利用hash算法得到key的hash值
* 这个位运算没看懂，根据注释应该是利用hash的低八位找到bucket
* 如果oldbuckets不为空，即正在执行扩容，所以优先从oldbuckets读取
* 根据hash的高8位遍历bucket，得到v。（这一大坨位运算没看懂。）

**修改**
```
//go:linkname reflect_mapassign reflect.mapassign
func reflect_mapassign(t *maptype, h *hmap, key unsafe.Pointer, val unsafe.Pointer) {
   p := mapassign(t, h, key)
   typedmemmove(t.elem, p, val)
}

// Like mapaccess, but allocates a slot for the key if it is not present in the map.
func mapassign(t *maptype, h *hmap, key unsafe.Pointer) unsafe.Pointer {}
```

put过程比较特别，之前说过bucket里面保存的是uint8数组，也就是指针。所以这里需要先给key找到对应的slot，然后将value拷贝到对应的地址。


# Atomic原子操作

**Background**

原子操作即执行过程不能被中断的操作（并发）。

经典问题：i++是不是原子操作？

答案是否，因为i++看上去只有一行，但是背后包括了多个操作：取值，加法，赋值。

**加/减**
```
atomic.AddInt32(&i, 1)
```
代码很好理解，原子地对i加1。

问题是：为什么加法需要原子性？

思考，在32位OS，操作long类型，是否是原子的？

答案是否，因为32位操作系统CPU一次只能操作32位数据，如果两个64位相加，那么首先会计算低32位，然后计算高32位。

除了操作系统原因，我觉得还有一个原因，因为仅仅i+1并不能对i加1，还必须赋值。

**CAS**

Compare And Swap，比较并交换，常见的原子操作。
```
func CompareAndSwapInt32(addr *int32, old, new int32) (swapped bool)
```
三个入参分别表示：被操作值的指针，被操作值的old值，被操作值的new值。

首先会判断指针指向的被操作值是否与old相等，如果相等就用new替换old，完成数据更新；否则忽略替换操作。整个过程都是原子性的。

Note：CAS与lock区别：

* CAS不需要创建互斥量，临界区，所以性能好于lock，这也是性能优化的一个点；
* CAS是乐观的，即认为old没有被并发修改，而lock是悲观的，总是认为old是并发不安全的；
* 如果old被并发修改了，CAS就不会成功。所以我们需要循环多次执行CAS操作，以让他生效，类似自旋。

**Load**

原子读取变量，防止变量值其他并发读写操作。

还是之前操作系统的例子，在32位操作系统，写入一个long，如果在这个写操作完成前（先改低32位，再改高32位），有一个并发读操作，这个读操作就可能会读取一个只被修改一般的数据。

**Store**
例子与之前类似。原子存储操作有一个特点，与CAS不同，存储总是成功的，它不关心old。
```
func StoreInt32(addr *int32, val int32)
```

**Swap**
与CAS不同，他不关心old；与Store不同，它会返回old。介于两者之间。
```
func SwapInt32(addr *int32, new int32) (old int32)
```
原子值
上面的原子操作都只支持基本类型，如果想对其他类型进行原子操作怎么办？所以Go提供了原子值类型，它对于类型没有限制。它支持Load和Store方法。
```
// A Value provides an atomic load and store of a consistently typed value.
// The zero value for a Value returns nil from Load.
// Once Store has been called, a Value must not be copied.
//
// A Value must not be copied after first use.
type Value struct {
    v interface{}
}
```
执行Store之后，Value禁止copy。目前已知的copy行为包括：赋值其他变量，函数入参，函数返回值，传入chan。
```
// Store sets the value of the Value to x.
// All calls to Store for a given Value must use values of the same concrete type.
// Store of an inconsistent type panics, as does Store(nil).
func (v *Value) Store(x interface{}) {
    if x == nil {
        panic("sync/atomic: store of nil value into Value")
    }
    vp := (*ifaceWords)(unsafe.Pointer(v))
    xp := (*ifaceWords)(unsafe.Pointer(&x))
    for {
        typ := LoadPointer(&vp.typ)
        if typ == nil {
            // Attempt to start first store.
            // Disable preemption so that other goroutines can use
            // active spin wait to wait for completion; and so that
            // GC does not see the fake type accidentally.
            runtime_procPin()
            if !CompareAndSwapPointer(&vp.typ, nil, unsafe.Pointer(^uintptr(0))) {
                runtime_procUnpin()
                continue
            }
            // Complete first store.
            StorePointer(&vp.data, xp.data)
            StorePointer(&vp.typ, xp.typ)
            runtime_procUnpin()
            return
        }
        if uintptr(typ) == ^uintptr(0) {
            // First store in progress. Wait.
            // Since we disable preemption around the first store,
            // we can wait with active spinning.
            continue
        }
        // First store completed. Check type and overwrite data.
        if typ != xp.typ {
            panic("sync/atomic: store of inconsistently typed value into Value")
        }
        StorePointer(&vp.data, xp.data)
        return
    }
}
}
```

store不允许nil，并且类型必须与第一次store一致，否则panic。


# sync.Map详解

sync.Map是1.9才推荐的并发安全的map，除了互斥量以外，还运用了原子操作，所以在这之前，有必要了解下Go语言——原子操作

源码 go1.10\src\sync\map.go

**Struct**

```
type Map struct {
   mu Mutex

   read atomic.Value // readOnly

   dirty map[interface{}]*entry

   misses int
}
var expunged = unsafe.Pointer(new(interface{}))
```

* read: readOnly, 保存了map中可以并发读的数据。并发写有可能不需要互斥，但是更新之前标记删除的数据（从一个value指针变成expunged指针），就需要将条目拷贝到dirty中，并且unexpunged操作（？还不懂什么意思，将expunged指针变成value指针？）需要锁。

* dirty: 脏数据需要锁。为了尽快提升为read，dirty需要保存read中所有未标记删除的数据（减少数据拷贝？）。标记删除的条目不保存的dirty里面（那就是保存在read里面咯）
* misses: 从read里面读，miss之后再从dirty里面读。当miss多次之后，就将dirty提升为read。

```
type entry struct {
   // If p == nil, the entry has been deleted and m.dirty == nil.
   //
   // If p == expunged, the entry has been deleted, m.dirty != nil, and the entry
   // is missing from m.dirty.
   //
   // Otherwise, the entry is valid and recorded in m.read.m[key] and, if m.dirty
   // != nil, in m.dirty[key].
   p unsafe.Pointer // *interface{}
}
```
entry分为三种情况：

* nil：已经被删除，并且dirty不存在
* expunged：已经被删除了，dirty存在，且条目不在dirty里面，标记删除
* 其他情况：保存在read和dirty（存在）中

**Store**
```
func (m *Map) Store(key, value interface{}) {
   read, _ := m.read.Load().(readOnly)
   if e, ok := read.m[key]; ok && e.tryStore(&value) {
      return
   }
```

从read中读取key，如果key存在就tryStore。

```
func (e *entry) tryStore(i *interface{}) bool {
   p := atomic.LoadPointer(&e.p)
   if p == expunged {
      return false
   }
   for {
      if atomic.CompareAndSwapPointer(&e.p, p, unsafe.Pointer(i)) {
         return true
      }
      p = atomic.LoadPointer(&e.p)
      if p == expunged {
         return false
      }
   }
}
```

* 原子地读取条目的值
* 如果条目被标记删除了（空接口指针），返回false；按照之前的逻辑，就是说如果条目被标记了，就继续store
* 尝试CAS新的value值，成功代表更新条目值成功。
* CAS失败，重新原子load，继续CAS，除非发现条目被其他的G标记了。
```
   m.mu.Lock()
   read, _ = m.read.Load().(readOnly)
   if e, ok := read.m[key]; ok {
      if e.unexpungeLocked() {
         m.dirty[key] = e
      }
      e.storeLocked(&value)
   }

func (e *entry) unexpungeLocked() (wasExpunged bool) {
   return atomic.CompareAndSwapPointer(&e.p, expunged, nil)
}

func (e *entry) storeLocked(i *interface{}) {
    atomic.StorePointer(&e.p, unsafe.Pointer(i))
}
```

注意这里开始需要加锁，因为需要操作dirty。

条目在read中，首先取消标记，然后将条目保存到dirty里。（因为标记的数据不在dirty里）

最后原子保存value到条目里面，这里注意read和dirty都有条目。
```
   else if e, ok := m.dirty[key]; ok {
      e.storeLocked(&value)
   } else {
      if !read.amended {
         m.dirtyLocked()
         m.read.Store(readOnly{m: read.m, amended: true})
      }
      m.dirty[key] = newEntry(value)
   }
   m.mu.Unlock()
}
```
* 如果条目在dirty里，就保存value。这里注意哈，read里没有这个条目，而dirty里面有。
* 其他情况，新增条目。将所有未标记的条目保存到dirty里面。

**总结一下Store：**

* 新增操作，将条目保存在dirty里
* 更新操作，在read中，如果没有被其他G标记，就直接在read里面更新
* 在read中，取消标记，保存到dirty中，并且赋值
* 在dirty中，就直接更新

这里可以看到dirty保存了数据的修改，除非可以直接原子更新read，继续保持read clean。

**Load**
有了之前的经验，可以猜测下load流程：

* 先从read里面直接读
* 加锁
* 更新miss
* 从dirty里面读
* 解锁
```
func (m *Map) Load(key interface{}) (value interface{}, ok bool) {
   read, _ := m.read.Load().(readOnly)
   e, ok := read.m[key]
   if !ok && read.amended {
      m.mu.Lock()
      // Avoid reporting a spurious miss if m.dirty got promoted while we were
      // blocked on m.mu. (If further loads of the same key will not miss, it's
      // not worth copying the dirty map for this key.)
      read, _ = m.read.Load().(readOnly)
      e, ok = read.m[key]
      if !ok && read.amended {
         e, ok = m.dirty[key]
         // Regardless of whether the entry was present, record a miss: this key
         // will take the slow path until the dirty map is promoted to the read
         // map.
         m.missLocked()
      }
      m.mu.Unlock()
   }
   if !ok {
      return nil, false
   }
   return e.load()
}

func (m *Map) missLocked() {
    m.misses++
    if m.misses < len(m.dirty) {
        return
    }
    m.read.Store(readOnly{m: m.dirty})
    m.dirty = nil
    m.misses = 0
}
```

与猜测的区别：

* 读了两次read，做了一个double-check
* 更新miss还有额外操作，即dirty升级；原来miss的阈值是dirty长度。

**Delete**

由于数据保存两份，所以删除考虑：

* read & dirty都有，干净的数据
* read没有，dirty有，dirty中还未升级的数据
* read有，dirty没有，标记删除的数据
```
func (m *Map) Delete(key interface{}) {
   read, _ := m.read.Load().(readOnly)
   e, ok := read.m[key]
   if !ok && read.amended {
      m.mu.Lock()
      read, _ = m.read.Load().(readOnly)
      e, ok = read.m[key]
      if !ok && read.amended {
         delete(m.dirty, key)
      }
      m.mu.Unlock()
   }
   if ok {
      e.delete()
   }
}
```

先看第二种情况。加锁直接删除dirty数据。思考下貌似没什么问题，本身就是脏数据。
```
func (e *entry) delete() (hadValue bool) {
   for {
      p := atomic.LoadPointer(&e.p)
      if p == nil || p == expunged {
         return false
      }
      if atomic.CompareAndSwapPointer(&e.p, p, nil) {
         return true
      }
   }
}
```

第一种和第三种情况唯一的区别就是条目是否被标记。标记代表删除，所以直接返回。否则CAS操作置为nil。这里总感觉少点什么，因为条目其实还是存在的，虽然指针nil。

**标记**
看了一圈貌似没找到标记的逻辑，因为删除只是将他变成nil。
```
func (e *entry) tryExpungeLocked() (isExpunged bool) {
   p := atomic.LoadPointer(&e.p)
   for p == nil {
      if atomic.CompareAndSwapPointer(&e.p, nil, expunged) {
         return true
      }
      p = atomic.LoadPointer(&e.p)
   }
   return p == expunged
}

func (m *Map) dirtyLocked() {
    if m.dirty != nil {
        return
    }

    read, _ := m.read.Load().(readOnly)
    m.dirty = make(map[interface{}]*entry, len(read.m))
    for k, e := range read.m {
        if !e.tryExpungeLocked() {
            m.dirty[k] = e
        }
    }
}
```
之前以为这个逻辑就是简单的将为标记的条目拷贝给dirty，现在看来大有文章。

p == nil，说明条目已经被delete了，CAS将他置为标记删除。然后这个条目就不会保存在dirty里面。
```
func (m *Map) missLocked() {
   m.misses++
   if m.misses < len(m.dirty) {
      return
   }
   m.read.Store(readOnly{m: m.dirty})
   m.dirty = nil
   m.misses = 0
}
```
这里其实就跟miss逻辑串起来了，因为miss达到阈值之后，dirty会全量变成read，也就是说标记删除在这一步最终删除。这个还是很巧妙的。

真正的删除逻辑：

* delete将条目变成nil
* store的时候，将nil的条目标记，并且这些条目不会存在于dirty中
* load的时候，如果miss达到阈值，就将dirty全量变成read，变现地删除了nil条目


# Sync.Once

[Once详解](https://mp.weixin.qq.com/s/Lsm-BMdKCKNQjRndNCLwLw)
[Once](https://pioneerlfn.github.io/2019/12/12/go-sync-Once/)


