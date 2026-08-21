<script>
  import { tooltip } from "@svelte-plugins/tooltips";
  import Dialog from "../baseComponents/dialog.svelte";
  import Button from "../baseComponents/Button.svelte";
  import Input from "../baseComponents/Input.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onDestroy, onMount } from "svelte";
  import { compile } from "svelte/compiler";
  import QRCode from "qrcode";

  let factorId;
  let codeInput = $state("");
  let secretValue = $state("");
  let factorName = $state("");
  let isError = $state(false);
  let qrCodeSrc = $state("");
  let open = $state(false);

  async function enroll() {
    await supabase.auth.refreshSession();
    const { data, error } = await supabase.auth.mfa.enroll({
      factorType: "totp",
      friendlyName: `mcPanel-${factorName}`,
    });

    console.warn("DATA : ", data);

    const {
      id,
      type,
      totp: { qr_code, secret, uri },
      friendly_name,
    } = data;
    factorId = id;
    qrCodeSrc = await generateQr(data.totp.uri, friendly_name);
    secretValue = secret;
    step = "qr";
  }

  function customizeTotpUri(uri, issuer, account) {
    const url = new URL(uri);

    url.searchParams.set("issuer", issuer);

    url.pathname = `/${encodeURIComponent(`${issuer}: ${account}`)}`;

    return url.toString();
  }

  async function generateQr(uri, friendlyName, account) {
    // Supabase QR code doesn't work for some reason.. TODO : check if it works regularly and switch back to it if it does
    const datas = await supabase.auth.getUser();
    const mail = datas.data.user.email;
    return await QRCode.toDataURL(customizeTotpUri(uri, friendlyName, mail));
  }

  async function challengeAndVerify() {
    const { data, error } = await supabase.auth.mfa.challengeAndVerify({
      factorId: factorId,
      code: codeInput,
    });
    if (error) {
      console.error("MFA enroll failed:", {
        name: error.name,
        message: error.message,
        status: error.status,
        code: error.code,
      });
      isError = true;
      return;
    }
    step = "complete";
  }

  onDestroy(async () => {
    if (step !== "complete" && open) {
      await supabase.auth.mfa.unenroll({
        factorId: factorId,
      });
    }
    step = "info";
    factorId = "";
    secretValue = "";
  });

  let step = $state("info");
  // Steps are info, qr, complete
  // TODO : Creating multiple steps dialog
</script>

<Dialog
  title="Authentification à deux facteurs"
  description={step != "complete"
    ? "Mettez en place l'authentification à deux facteurs en passant par une application d'authentification."
    : ""}
  name="TOTPEnrollmentDialog"
  contentClass="flex flex-col items-center"
  bind:open
>
  {#if step == "info"}
    <Button onclick={() => (step = "factorName")}>Commencer</Button>
  {:else if step == "factorName"}
    <span>Entrez un nom unique et reconnaissable pour votre code.</span>
    <Input label="nom" placeholder="téléphone" bind:value={factorName} />
    <Button onclick={enroll}>Valider</Button>
  {:else if step == "qr"}
    <img
      src={qrCodeSrc}
      height="300px"
      width="300px"
      class="qrCode"
      alt="Qr code d'authentification"
    />
    <span>Ou utilisez le code : {secretValue}</span>
    {#if isError}
      <span class="error">Code invalide</span>
    {/if}
    <Input
      label="Code d'authentification"
      bind:value={codeInput}
      placeholder="123456"
    />
    <Button onclick={challengeAndVerify}>Valider</Button>
  {:else if step == "complete"}
    <h2>Enregistrement terminé!</h2>
    <span
      >Notre fournisseur d'authentification ne nous permet pas de proposer des
      codes de vérification. Vous pouvez utiliser plusieurs applications
      d'authentification pour garantir l'accès à votre compte.</span
    >
  {/if}
</Dialog>

<style>
  .error {
    color: var(--dangerous);
    font-size: 0.9rem;
  }

  span {
    font-size: 0.9rem;
  }
</style>
