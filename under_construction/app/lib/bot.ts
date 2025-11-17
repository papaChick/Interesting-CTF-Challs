export async function launchChromium(
  url: string,
  callback?: (status: Deno.CommandStatus | null, error?: unknown) => void
) {
  const userDataDir = await Deno.makeTempDir({ prefix: 'chromium-temp-profile-' });
  const process = new Deno.Command('chromium', {
    args: [
      url,
      '--headless',
      '--disable-gpu',
      '--no-sandbox',
      '--disable-popup-blocking',
      '--disable-features=HttpsUpgrades',
      `--user-data-dir=${userDataDir}`,
      '--ignore-certificate-errors',
    ],
    stdout: 'null',
    stderr: 'null',
  }).spawn();

  const timer = setTimeout(() => {
    try {
      process.kill('SIGTERM');
    } catch {
      console.warn('already exited');
    }
  }, 20_000);

  let status: Deno.CommandStatus | null = null;
  let error: unknown = null;

  try {
    status = await process.status;
  } catch (err) {
    error = err;
  } finally {
    clearTimeout(timer);
    if (callback) callback(status, error);
  }
}
