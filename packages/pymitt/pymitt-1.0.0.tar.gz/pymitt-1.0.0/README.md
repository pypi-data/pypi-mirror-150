
# pymitt

### A minimal Python wrapper for Keymitt webhooks

Usage is super simple. Import the script, and initialize as many Keymitt locks or push buttons as you like by providing the device's ID and token.
Needs an event loop to run.

Minimal example to lock and unlock a Keymitt lock from a simple script:


    import asyncio

    from pymitt import pymitt

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    k = pymitt.KeymittLock("YOUR_LOCK_ID", "YOUR_TOKEN")

    # Lock the lock
    loop.run_until_complete(k.lock())

    # Unlock the lock
    loop.run_until_complete(k.unlock())
