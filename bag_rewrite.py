import rosbags
import rosbags.rosbag2
import rosbags.typesys.stores
import rosbags.typesys.store
import argparse

def work(
    reader: rosbags.rosbag2.Reader,
    writer: rosbags.rosbag2.Writer,
    input_typestore: rosbags.typesys.store.Typestore,
    output_typestore: rosbags.typesys.store.Typestore):
  for conn, ns, msg in reader.messages():
    print(f"[{ns / 10**9:.9f}]: {conn.topic}")


def get_default_store():
  import os
  version = os.environ.get("ROS_VERSION")
  distro = os.environ.get("ROS_DISTRO")
  default_store = f'ros{version}_{distro}'.lower()

  try:
    return rosbags.typesys.Stores(default_store)
  except ValueError:
    return None

default_store = get_default_store()

parser = argparse.ArgumentParser()
parser.add_argument("input_path")
parser.add_argument("output_path")
store_kwargs = {
  'default': default_store,
  'required': default_store is None
}
parser.add_argument("--input_typestore", type=rosbags.typesys.Stores, **store_kwargs)
parser.add_argument("--output_typestore", type=rosbags.typesys.Stores, **store_kwargs)
args = parser.parse_args()

with rosbags.rosbag2.Reader(args.input_path) as reader:
 with rosbags.rosbag2.Writer(args.output_path) as writer:
    work(
      reader,
      writer,
      rosbags.typesys.stores.get_typestore(args.input_typestore),
      rosbags.typesys.stores.get_typestore(args.output_typestore)
    )