To increase swap memory on your machine, you need to adjust the swap settings at the operating system level. Here's how you can do it for **Linux** systems (the most common environment for Docker):

### Steps to Increase Swap Memory

#### 1. **Check the Current Swap Size**

First, check the current swap size using the following command:

```bash
swapon --show
```

This will show you the current swap devices and their sizes.

You can also check memory and swap usage with:

```bash
free -h
```

#### 2. **Turn Off Current Swap (Optional)**

If you want to increase swap space by replacing the current swap file or partition, you'll need to turn off the swap before modifying it.

```bash
sudo swapoff -a
```

#### 3. **Create a New Swap File**

If you don't already have a swap file or want to increase the swap space, you can create a new swap file.

- For example, to create a 4 GB swap file:

```bash
sudo dd if=/dev/zero of=/swapfile bs=1G count=4
```

This command will create a swap file named `/swapfile` with a size of 4 GB. You can adjust `count=4` to your desired size (e.g., `count=8` for 8 GB).

#### 4. **Set the Correct Permissions**

Make the swap file secure by setting the appropriate permissions:

```bash
sudo chmod 600 /swapfile
```

#### 5. **Mark the File as Swap**

After creating the file, you need to mark it as a swap area:

```bash
sudo mkswap /swapfile
```

#### 6. **Enable the Swap**

Now, enable the newly created swap file:

```bash
sudo swapon /swapfile
```

You can verify it's working by running:

```bash
swapon --show
```

This will now show the new swap size.
