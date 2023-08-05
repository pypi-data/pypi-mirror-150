// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/util/memmapped_file_system.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3009000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3009002 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[2]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto;
namespace tensorflow {
class MemmappedFileSystemDirectory;
class MemmappedFileSystemDirectoryDefaultTypeInternal;
extern MemmappedFileSystemDirectoryDefaultTypeInternal _MemmappedFileSystemDirectory_default_instance_;
class MemmappedFileSystemDirectoryElement;
class MemmappedFileSystemDirectoryElementDefaultTypeInternal;
extern MemmappedFileSystemDirectoryElementDefaultTypeInternal _MemmappedFileSystemDirectoryElement_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::MemmappedFileSystemDirectory* Arena::CreateMaybeMessage<::tensorflow::MemmappedFileSystemDirectory>(Arena*);
template<> ::tensorflow::MemmappedFileSystemDirectoryElement* Arena::CreateMaybeMessage<::tensorflow::MemmappedFileSystemDirectoryElement>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class MemmappedFileSystemDirectoryElement :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.MemmappedFileSystemDirectoryElement) */ {
 public:
  MemmappedFileSystemDirectoryElement();
  virtual ~MemmappedFileSystemDirectoryElement();

  MemmappedFileSystemDirectoryElement(const MemmappedFileSystemDirectoryElement& from);
  MemmappedFileSystemDirectoryElement(MemmappedFileSystemDirectoryElement&& from) noexcept
    : MemmappedFileSystemDirectoryElement() {
    *this = ::std::move(from);
  }

  inline MemmappedFileSystemDirectoryElement& operator=(const MemmappedFileSystemDirectoryElement& from) {
    CopyFrom(from);
    return *this;
  }
  inline MemmappedFileSystemDirectoryElement& operator=(MemmappedFileSystemDirectoryElement&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArena() const final {
    return GetArenaNoVirtual();
  }
  inline void* GetMaybeArenaPointer() const final {
    return MaybeArenaPtr();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const MemmappedFileSystemDirectoryElement& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const MemmappedFileSystemDirectoryElement* internal_default_instance() {
    return reinterpret_cast<const MemmappedFileSystemDirectoryElement*>(
               &_MemmappedFileSystemDirectoryElement_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(MemmappedFileSystemDirectoryElement& a, MemmappedFileSystemDirectoryElement& b) {
    a.Swap(&b);
  }
  inline void Swap(MemmappedFileSystemDirectoryElement* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(MemmappedFileSystemDirectoryElement* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline MemmappedFileSystemDirectoryElement* New() const final {
    return CreateMaybeMessage<MemmappedFileSystemDirectoryElement>(nullptr);
  }

  MemmappedFileSystemDirectoryElement* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<MemmappedFileSystemDirectoryElement>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const MemmappedFileSystemDirectoryElement& from);
  void MergeFrom(const MemmappedFileSystemDirectoryElement& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(MemmappedFileSystemDirectoryElement* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.MemmappedFileSystemDirectoryElement";
  }
  protected:
  explicit MemmappedFileSystemDirectoryElement(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kNameFieldNumber = 2,
    kOffsetFieldNumber = 1,
    kLengthFieldNumber = 3,
  };
  // string name = 2;
  void clear_name();
  const std::string& name() const;
  void set_name(const std::string& value);
  void set_name(std::string&& value);
  void set_name(const char* value);
  void set_name(const char* value, size_t size);
  std::string* mutable_name();
  std::string* release_name();
  void set_allocated_name(std::string* name);
  GOOGLE_PROTOBUF_RUNTIME_DEPRECATED("The unsafe_arena_ accessors for"
  "    string fields are deprecated and will be removed in a"
  "    future release.")
  std::string* unsafe_arena_release_name();
  GOOGLE_PROTOBUF_RUNTIME_DEPRECATED("The unsafe_arena_ accessors for"
  "    string fields are deprecated and will be removed in a"
  "    future release.")
  void unsafe_arena_set_allocated_name(
      std::string* name);

  // uint64 offset = 1;
  void clear_offset();
  ::PROTOBUF_NAMESPACE_ID::uint64 offset() const;
  void set_offset(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // uint64 length = 3;
  void clear_length();
  ::PROTOBUF_NAMESPACE_ID::uint64 length() const;
  void set_length(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // @@protoc_insertion_point(class_scope:tensorflow.MemmappedFileSystemDirectoryElement)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
  ::PROTOBUF_NAMESPACE_ID::uint64 offset_;
  ::PROTOBUF_NAMESPACE_ID::uint64 length_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto;
};
// -------------------------------------------------------------------

class MemmappedFileSystemDirectory :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.MemmappedFileSystemDirectory) */ {
 public:
  MemmappedFileSystemDirectory();
  virtual ~MemmappedFileSystemDirectory();

  MemmappedFileSystemDirectory(const MemmappedFileSystemDirectory& from);
  MemmappedFileSystemDirectory(MemmappedFileSystemDirectory&& from) noexcept
    : MemmappedFileSystemDirectory() {
    *this = ::std::move(from);
  }

  inline MemmappedFileSystemDirectory& operator=(const MemmappedFileSystemDirectory& from) {
    CopyFrom(from);
    return *this;
  }
  inline MemmappedFileSystemDirectory& operator=(MemmappedFileSystemDirectory&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArena() const final {
    return GetArenaNoVirtual();
  }
  inline void* GetMaybeArenaPointer() const final {
    return MaybeArenaPtr();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const MemmappedFileSystemDirectory& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const MemmappedFileSystemDirectory* internal_default_instance() {
    return reinterpret_cast<const MemmappedFileSystemDirectory*>(
               &_MemmappedFileSystemDirectory_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(MemmappedFileSystemDirectory& a, MemmappedFileSystemDirectory& b) {
    a.Swap(&b);
  }
  inline void Swap(MemmappedFileSystemDirectory* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(MemmappedFileSystemDirectory* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline MemmappedFileSystemDirectory* New() const final {
    return CreateMaybeMessage<MemmappedFileSystemDirectory>(nullptr);
  }

  MemmappedFileSystemDirectory* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<MemmappedFileSystemDirectory>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const MemmappedFileSystemDirectory& from);
  void MergeFrom(const MemmappedFileSystemDirectory& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(MemmappedFileSystemDirectory* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.MemmappedFileSystemDirectory";
  }
  protected:
  explicit MemmappedFileSystemDirectory(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kElementFieldNumber = 1,
  };
  // repeated .tensorflow.MemmappedFileSystemDirectoryElement element = 1;
  int element_size() const;
  void clear_element();
  ::tensorflow::MemmappedFileSystemDirectoryElement* mutable_element(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::MemmappedFileSystemDirectoryElement >*
      mutable_element();
  const ::tensorflow::MemmappedFileSystemDirectoryElement& element(int index) const;
  ::tensorflow::MemmappedFileSystemDirectoryElement* add_element();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::MemmappedFileSystemDirectoryElement >&
      element() const;

  // @@protoc_insertion_point(class_scope:tensorflow.MemmappedFileSystemDirectory)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::MemmappedFileSystemDirectoryElement > element_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// MemmappedFileSystemDirectoryElement

// uint64 offset = 1;
inline void MemmappedFileSystemDirectoryElement::clear_offset() {
  offset_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 MemmappedFileSystemDirectoryElement::offset() const {
  // @@protoc_insertion_point(field_get:tensorflow.MemmappedFileSystemDirectoryElement.offset)
  return offset_;
}
inline void MemmappedFileSystemDirectoryElement::set_offset(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  offset_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.MemmappedFileSystemDirectoryElement.offset)
}

// string name = 2;
inline void MemmappedFileSystemDirectoryElement::clear_name() {
  name_.ClearToEmpty(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaNoVirtual());
}
inline const std::string& MemmappedFileSystemDirectoryElement::name() const {
  // @@protoc_insertion_point(field_get:tensorflow.MemmappedFileSystemDirectoryElement.name)
  return name_.Get();
}
inline void MemmappedFileSystemDirectoryElement::set_name(const std::string& value) {
  
  name_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), value, GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set:tensorflow.MemmappedFileSystemDirectoryElement.name)
}
inline void MemmappedFileSystemDirectoryElement::set_name(std::string&& value) {
  
  name_.Set(
    &::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::move(value), GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_rvalue:tensorflow.MemmappedFileSystemDirectoryElement.name)
}
inline void MemmappedFileSystemDirectoryElement::set_name(const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  
  name_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::string(value),
              GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_char:tensorflow.MemmappedFileSystemDirectoryElement.name)
}
inline void MemmappedFileSystemDirectoryElement::set_name(const char* value,
    size_t size) {
  
  name_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::string(
      reinterpret_cast<const char*>(value), size), GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_pointer:tensorflow.MemmappedFileSystemDirectoryElement.name)
}
inline std::string* MemmappedFileSystemDirectoryElement::mutable_name() {
  
  // @@protoc_insertion_point(field_mutable:tensorflow.MemmappedFileSystemDirectoryElement.name)
  return name_.Mutable(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaNoVirtual());
}
inline std::string* MemmappedFileSystemDirectoryElement::release_name() {
  // @@protoc_insertion_point(field_release:tensorflow.MemmappedFileSystemDirectoryElement.name)
  
  return name_.Release(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaNoVirtual());
}
inline void MemmappedFileSystemDirectoryElement::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  name_.SetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), name,
      GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_allocated:tensorflow.MemmappedFileSystemDirectoryElement.name)
}
inline std::string* MemmappedFileSystemDirectoryElement::unsafe_arena_release_name() {
  // @@protoc_insertion_point(field_unsafe_arena_release:tensorflow.MemmappedFileSystemDirectoryElement.name)
  GOOGLE_DCHECK(GetArenaNoVirtual() != nullptr);
  
  return name_.UnsafeArenaRelease(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(),
      GetArenaNoVirtual());
}
inline void MemmappedFileSystemDirectoryElement::unsafe_arena_set_allocated_name(
    std::string* name) {
  GOOGLE_DCHECK(GetArenaNoVirtual() != nullptr);
  if (name != nullptr) {
    
  } else {
    
  }
  name_.UnsafeArenaSetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(),
      name, GetArenaNoVirtual());
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.MemmappedFileSystemDirectoryElement.name)
}

// uint64 length = 3;
inline void MemmappedFileSystemDirectoryElement::clear_length() {
  length_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 MemmappedFileSystemDirectoryElement::length() const {
  // @@protoc_insertion_point(field_get:tensorflow.MemmappedFileSystemDirectoryElement.length)
  return length_;
}
inline void MemmappedFileSystemDirectoryElement::set_length(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  length_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.MemmappedFileSystemDirectoryElement.length)
}

// -------------------------------------------------------------------

// MemmappedFileSystemDirectory

// repeated .tensorflow.MemmappedFileSystemDirectoryElement element = 1;
inline int MemmappedFileSystemDirectory::element_size() const {
  return element_.size();
}
inline void MemmappedFileSystemDirectory::clear_element() {
  element_.Clear();
}
inline ::tensorflow::MemmappedFileSystemDirectoryElement* MemmappedFileSystemDirectory::mutable_element(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.MemmappedFileSystemDirectory.element)
  return element_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::MemmappedFileSystemDirectoryElement >*
MemmappedFileSystemDirectory::mutable_element() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.MemmappedFileSystemDirectory.element)
  return &element_;
}
inline const ::tensorflow::MemmappedFileSystemDirectoryElement& MemmappedFileSystemDirectory::element(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.MemmappedFileSystemDirectory.element)
  return element_.Get(index);
}
inline ::tensorflow::MemmappedFileSystemDirectoryElement* MemmappedFileSystemDirectory::add_element() {
  // @@protoc_insertion_point(field_add:tensorflow.MemmappedFileSystemDirectory.element)
  return element_.Add();
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::MemmappedFileSystemDirectoryElement >&
MemmappedFileSystemDirectory::element() const {
  // @@protoc_insertion_point(field_list:tensorflow.MemmappedFileSystemDirectory.element)
  return element_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2futil_2fmemmapped_5ffile_5fsystem_2eproto
