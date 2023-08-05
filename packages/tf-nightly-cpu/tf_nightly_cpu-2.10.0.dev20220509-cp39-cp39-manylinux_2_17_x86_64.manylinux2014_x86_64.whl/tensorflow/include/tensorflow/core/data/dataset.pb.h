// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/data/dataset.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fdata_2fdataset_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fdata_2fdataset_2eproto

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
#include "tensorflow/core/framework/tensor.pb.h"
#include "tensorflow/core/framework/tensor_shape.pb.h"
#include "tensorflow/core/framework/types.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fdata_2fdataset_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fdata_2fdataset_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[3]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto;
namespace tensorflow {
namespace data {
class CompressedComponentMetadata;
class CompressedComponentMetadataDefaultTypeInternal;
extern CompressedComponentMetadataDefaultTypeInternal _CompressedComponentMetadata_default_instance_;
class CompressedElement;
class CompressedElementDefaultTypeInternal;
extern CompressedElementDefaultTypeInternal _CompressedElement_default_instance_;
class UncompressedElement;
class UncompressedElementDefaultTypeInternal;
extern UncompressedElementDefaultTypeInternal _UncompressedElement_default_instance_;
}  // namespace data
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::data::CompressedComponentMetadata* Arena::CreateMaybeMessage<::tensorflow::data::CompressedComponentMetadata>(Arena*);
template<> ::tensorflow::data::CompressedElement* Arena::CreateMaybeMessage<::tensorflow::data::CompressedElement>(Arena*);
template<> ::tensorflow::data::UncompressedElement* Arena::CreateMaybeMessage<::tensorflow::data::UncompressedElement>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {
namespace data {

// ===================================================================

class CompressedComponentMetadata :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.data.CompressedComponentMetadata) */ {
 public:
  CompressedComponentMetadata();
  virtual ~CompressedComponentMetadata();

  CompressedComponentMetadata(const CompressedComponentMetadata& from);
  CompressedComponentMetadata(CompressedComponentMetadata&& from) noexcept
    : CompressedComponentMetadata() {
    *this = ::std::move(from);
  }

  inline CompressedComponentMetadata& operator=(const CompressedComponentMetadata& from) {
    CopyFrom(from);
    return *this;
  }
  inline CompressedComponentMetadata& operator=(CompressedComponentMetadata&& from) noexcept {
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
  static const CompressedComponentMetadata& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const CompressedComponentMetadata* internal_default_instance() {
    return reinterpret_cast<const CompressedComponentMetadata*>(
               &_CompressedComponentMetadata_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(CompressedComponentMetadata& a, CompressedComponentMetadata& b) {
    a.Swap(&b);
  }
  inline void Swap(CompressedComponentMetadata* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(CompressedComponentMetadata* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline CompressedComponentMetadata* New() const final {
    return CreateMaybeMessage<CompressedComponentMetadata>(nullptr);
  }

  CompressedComponentMetadata* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<CompressedComponentMetadata>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const CompressedComponentMetadata& from);
  void MergeFrom(const CompressedComponentMetadata& from);
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
  void InternalSwap(CompressedComponentMetadata* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.data.CompressedComponentMetadata";
  }
  protected:
  explicit CompressedComponentMetadata(::PROTOBUF_NAMESPACE_ID::Arena* arena);
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
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kTensorShapeFieldNumber = 2,
    kTensorSizeBytesFieldNumber = 3,
    kDtypeFieldNumber = 1,
  };
  // .tensorflow.TensorShapeProto tensor_shape = 2;
  bool has_tensor_shape() const;
  void clear_tensor_shape();
  const ::tensorflow::TensorShapeProto& tensor_shape() const;
  ::tensorflow::TensorShapeProto* release_tensor_shape();
  ::tensorflow::TensorShapeProto* mutable_tensor_shape();
  void set_allocated_tensor_shape(::tensorflow::TensorShapeProto* tensor_shape);
  void unsafe_arena_set_allocated_tensor_shape(
      ::tensorflow::TensorShapeProto* tensor_shape);
  ::tensorflow::TensorShapeProto* unsafe_arena_release_tensor_shape();

  // int64 tensor_size_bytes = 3;
  void clear_tensor_size_bytes();
  ::PROTOBUF_NAMESPACE_ID::int64 tensor_size_bytes() const;
  void set_tensor_size_bytes(::PROTOBUF_NAMESPACE_ID::int64 value);

  // .tensorflow.DataType dtype = 1;
  void clear_dtype();
  ::tensorflow::DataType dtype() const;
  void set_dtype(::tensorflow::DataType value);

  // @@protoc_insertion_point(class_scope:tensorflow.data.CompressedComponentMetadata)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::tensorflow::TensorShapeProto* tensor_shape_;
  ::PROTOBUF_NAMESPACE_ID::int64 tensor_size_bytes_;
  int dtype_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fdata_2fdataset_2eproto;
};
// -------------------------------------------------------------------

class CompressedElement :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.data.CompressedElement) */ {
 public:
  CompressedElement();
  virtual ~CompressedElement();

  CompressedElement(const CompressedElement& from);
  CompressedElement(CompressedElement&& from) noexcept
    : CompressedElement() {
    *this = ::std::move(from);
  }

  inline CompressedElement& operator=(const CompressedElement& from) {
    CopyFrom(from);
    return *this;
  }
  inline CompressedElement& operator=(CompressedElement&& from) noexcept {
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
  static const CompressedElement& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const CompressedElement* internal_default_instance() {
    return reinterpret_cast<const CompressedElement*>(
               &_CompressedElement_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(CompressedElement& a, CompressedElement& b) {
    a.Swap(&b);
  }
  inline void Swap(CompressedElement* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(CompressedElement* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline CompressedElement* New() const final {
    return CreateMaybeMessage<CompressedElement>(nullptr);
  }

  CompressedElement* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<CompressedElement>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const CompressedElement& from);
  void MergeFrom(const CompressedElement& from);
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
  void InternalSwap(CompressedElement* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.data.CompressedElement";
  }
  protected:
  explicit CompressedElement(::PROTOBUF_NAMESPACE_ID::Arena* arena);
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
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kComponentMetadataFieldNumber = 2,
    kDataFieldNumber = 1,
  };
  // repeated .tensorflow.data.CompressedComponentMetadata component_metadata = 2;
  int component_metadata_size() const;
  void clear_component_metadata();
  ::tensorflow::data::CompressedComponentMetadata* mutable_component_metadata(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::data::CompressedComponentMetadata >*
      mutable_component_metadata();
  const ::tensorflow::data::CompressedComponentMetadata& component_metadata(int index) const;
  ::tensorflow::data::CompressedComponentMetadata* add_component_metadata();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::data::CompressedComponentMetadata >&
      component_metadata() const;

  // bytes data = 1;
  void clear_data();
  const std::string& data() const;
  void set_data(const std::string& value);
  void set_data(std::string&& value);
  void set_data(const char* value);
  void set_data(const void* value, size_t size);
  std::string* mutable_data();
  std::string* release_data();
  void set_allocated_data(std::string* data);
  GOOGLE_PROTOBUF_RUNTIME_DEPRECATED("The unsafe_arena_ accessors for"
  "    string fields are deprecated and will be removed in a"
  "    future release.")
  std::string* unsafe_arena_release_data();
  GOOGLE_PROTOBUF_RUNTIME_DEPRECATED("The unsafe_arena_ accessors for"
  "    string fields are deprecated and will be removed in a"
  "    future release.")
  void unsafe_arena_set_allocated_data(
      std::string* data);

  // @@protoc_insertion_point(class_scope:tensorflow.data.CompressedElement)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::data::CompressedComponentMetadata > component_metadata_;
  ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr data_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fdata_2fdataset_2eproto;
};
// -------------------------------------------------------------------

class UncompressedElement :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.data.UncompressedElement) */ {
 public:
  UncompressedElement();
  virtual ~UncompressedElement();

  UncompressedElement(const UncompressedElement& from);
  UncompressedElement(UncompressedElement&& from) noexcept
    : UncompressedElement() {
    *this = ::std::move(from);
  }

  inline UncompressedElement& operator=(const UncompressedElement& from) {
    CopyFrom(from);
    return *this;
  }
  inline UncompressedElement& operator=(UncompressedElement&& from) noexcept {
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
  static const UncompressedElement& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const UncompressedElement* internal_default_instance() {
    return reinterpret_cast<const UncompressedElement*>(
               &_UncompressedElement_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    2;

  friend void swap(UncompressedElement& a, UncompressedElement& b) {
    a.Swap(&b);
  }
  inline void Swap(UncompressedElement* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(UncompressedElement* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline UncompressedElement* New() const final {
    return CreateMaybeMessage<UncompressedElement>(nullptr);
  }

  UncompressedElement* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<UncompressedElement>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const UncompressedElement& from);
  void MergeFrom(const UncompressedElement& from);
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
  void InternalSwap(UncompressedElement* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.data.UncompressedElement";
  }
  protected:
  explicit UncompressedElement(::PROTOBUF_NAMESPACE_ID::Arena* arena);
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
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fdata_2fdataset_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kComponentsFieldNumber = 1,
  };
  // repeated .tensorflow.TensorProto components = 1;
  int components_size() const;
  void clear_components();
  ::tensorflow::TensorProto* mutable_components(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorProto >*
      mutable_components();
  const ::tensorflow::TensorProto& components(int index) const;
  ::tensorflow::TensorProto* add_components();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorProto >&
      components() const;

  // @@protoc_insertion_point(class_scope:tensorflow.data.UncompressedElement)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorProto > components_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fdata_2fdataset_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// CompressedComponentMetadata

// .tensorflow.DataType dtype = 1;
inline void CompressedComponentMetadata::clear_dtype() {
  dtype_ = 0;
}
inline ::tensorflow::DataType CompressedComponentMetadata::dtype() const {
  // @@protoc_insertion_point(field_get:tensorflow.data.CompressedComponentMetadata.dtype)
  return static_cast< ::tensorflow::DataType >(dtype_);
}
inline void CompressedComponentMetadata::set_dtype(::tensorflow::DataType value) {
  
  dtype_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.data.CompressedComponentMetadata.dtype)
}

// .tensorflow.TensorShapeProto tensor_shape = 2;
inline bool CompressedComponentMetadata::has_tensor_shape() const {
  return this != internal_default_instance() && tensor_shape_ != nullptr;
}
inline const ::tensorflow::TensorShapeProto& CompressedComponentMetadata::tensor_shape() const {
  const ::tensorflow::TensorShapeProto* p = tensor_shape_;
  // @@protoc_insertion_point(field_get:tensorflow.data.CompressedComponentMetadata.tensor_shape)
  return p != nullptr ? *p : *reinterpret_cast<const ::tensorflow::TensorShapeProto*>(
      &::tensorflow::_TensorShapeProto_default_instance_);
}
inline ::tensorflow::TensorShapeProto* CompressedComponentMetadata::release_tensor_shape() {
  // @@protoc_insertion_point(field_release:tensorflow.data.CompressedComponentMetadata.tensor_shape)
  
  ::tensorflow::TensorShapeProto* temp = tensor_shape_;
  if (GetArenaNoVirtual() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
  tensor_shape_ = nullptr;
  return temp;
}
inline ::tensorflow::TensorShapeProto* CompressedComponentMetadata::unsafe_arena_release_tensor_shape() {
  // @@protoc_insertion_point(field_unsafe_arena_release:tensorflow.data.CompressedComponentMetadata.tensor_shape)
  
  ::tensorflow::TensorShapeProto* temp = tensor_shape_;
  tensor_shape_ = nullptr;
  return temp;
}
inline ::tensorflow::TensorShapeProto* CompressedComponentMetadata::mutable_tensor_shape() {
  
  if (tensor_shape_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::TensorShapeProto>(GetArenaNoVirtual());
    tensor_shape_ = p;
  }
  // @@protoc_insertion_point(field_mutable:tensorflow.data.CompressedComponentMetadata.tensor_shape)
  return tensor_shape_;
}
inline void CompressedComponentMetadata::set_allocated_tensor_shape(::tensorflow::TensorShapeProto* tensor_shape) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(tensor_shape_);
  }
  if (tensor_shape) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
      reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(tensor_shape)->GetArena();
    if (message_arena != submessage_arena) {
      tensor_shape = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, tensor_shape, submessage_arena);
    }
    
  } else {
    
  }
  tensor_shape_ = tensor_shape;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.data.CompressedComponentMetadata.tensor_shape)
}

// int64 tensor_size_bytes = 3;
inline void CompressedComponentMetadata::clear_tensor_size_bytes() {
  tensor_size_bytes_ = PROTOBUF_LONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::int64 CompressedComponentMetadata::tensor_size_bytes() const {
  // @@protoc_insertion_point(field_get:tensorflow.data.CompressedComponentMetadata.tensor_size_bytes)
  return tensor_size_bytes_;
}
inline void CompressedComponentMetadata::set_tensor_size_bytes(::PROTOBUF_NAMESPACE_ID::int64 value) {
  
  tensor_size_bytes_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.data.CompressedComponentMetadata.tensor_size_bytes)
}

// -------------------------------------------------------------------

// CompressedElement

// bytes data = 1;
inline void CompressedElement::clear_data() {
  data_.ClearToEmpty(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaNoVirtual());
}
inline const std::string& CompressedElement::data() const {
  // @@protoc_insertion_point(field_get:tensorflow.data.CompressedElement.data)
  return data_.Get();
}
inline void CompressedElement::set_data(const std::string& value) {
  
  data_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), value, GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set:tensorflow.data.CompressedElement.data)
}
inline void CompressedElement::set_data(std::string&& value) {
  
  data_.Set(
    &::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::move(value), GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_rvalue:tensorflow.data.CompressedElement.data)
}
inline void CompressedElement::set_data(const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  
  data_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::string(value),
              GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_char:tensorflow.data.CompressedElement.data)
}
inline void CompressedElement::set_data(const void* value,
    size_t size) {
  
  data_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::string(
      reinterpret_cast<const char*>(value), size), GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_pointer:tensorflow.data.CompressedElement.data)
}
inline std::string* CompressedElement::mutable_data() {
  
  // @@protoc_insertion_point(field_mutable:tensorflow.data.CompressedElement.data)
  return data_.Mutable(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaNoVirtual());
}
inline std::string* CompressedElement::release_data() {
  // @@protoc_insertion_point(field_release:tensorflow.data.CompressedElement.data)
  
  return data_.Release(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaNoVirtual());
}
inline void CompressedElement::set_allocated_data(std::string* data) {
  if (data != nullptr) {
    
  } else {
    
  }
  data_.SetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), data,
      GetArenaNoVirtual());
  // @@protoc_insertion_point(field_set_allocated:tensorflow.data.CompressedElement.data)
}
inline std::string* CompressedElement::unsafe_arena_release_data() {
  // @@protoc_insertion_point(field_unsafe_arena_release:tensorflow.data.CompressedElement.data)
  GOOGLE_DCHECK(GetArenaNoVirtual() != nullptr);
  
  return data_.UnsafeArenaRelease(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(),
      GetArenaNoVirtual());
}
inline void CompressedElement::unsafe_arena_set_allocated_data(
    std::string* data) {
  GOOGLE_DCHECK(GetArenaNoVirtual() != nullptr);
  if (data != nullptr) {
    
  } else {
    
  }
  data_.UnsafeArenaSetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(),
      data, GetArenaNoVirtual());
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.data.CompressedElement.data)
}

// repeated .tensorflow.data.CompressedComponentMetadata component_metadata = 2;
inline int CompressedElement::component_metadata_size() const {
  return component_metadata_.size();
}
inline void CompressedElement::clear_component_metadata() {
  component_metadata_.Clear();
}
inline ::tensorflow::data::CompressedComponentMetadata* CompressedElement::mutable_component_metadata(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.data.CompressedElement.component_metadata)
  return component_metadata_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::data::CompressedComponentMetadata >*
CompressedElement::mutable_component_metadata() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.data.CompressedElement.component_metadata)
  return &component_metadata_;
}
inline const ::tensorflow::data::CompressedComponentMetadata& CompressedElement::component_metadata(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.data.CompressedElement.component_metadata)
  return component_metadata_.Get(index);
}
inline ::tensorflow::data::CompressedComponentMetadata* CompressedElement::add_component_metadata() {
  // @@protoc_insertion_point(field_add:tensorflow.data.CompressedElement.component_metadata)
  return component_metadata_.Add();
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::data::CompressedComponentMetadata >&
CompressedElement::component_metadata() const {
  // @@protoc_insertion_point(field_list:tensorflow.data.CompressedElement.component_metadata)
  return component_metadata_;
}

// -------------------------------------------------------------------

// UncompressedElement

// repeated .tensorflow.TensorProto components = 1;
inline int UncompressedElement::components_size() const {
  return components_.size();
}
inline ::tensorflow::TensorProto* UncompressedElement::mutable_components(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.data.UncompressedElement.components)
  return components_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorProto >*
UncompressedElement::mutable_components() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.data.UncompressedElement.components)
  return &components_;
}
inline const ::tensorflow::TensorProto& UncompressedElement::components(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.data.UncompressedElement.components)
  return components_.Get(index);
}
inline ::tensorflow::TensorProto* UncompressedElement::add_components() {
  // @@protoc_insertion_point(field_add:tensorflow.data.UncompressedElement.components)
  return components_.Add();
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorProto >&
UncompressedElement::components() const {
  // @@protoc_insertion_point(field_list:tensorflow.data.UncompressedElement.components)
  return components_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------

// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace data
}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fdata_2fdataset_2eproto
