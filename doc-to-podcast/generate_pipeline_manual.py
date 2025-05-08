from kfp import dsl, compiler, components


download_document = components.load_component_from_file("./_components/downloader.yaml")
transform_document = components.load_component_from_file("./_components/transformer.yaml")
scriptwriter = components.load_component_from_file("./_components/scriptwriter.yaml")
performer = components.load_component_from_file("./_components/performer.yaml")


@dsl.pipeline
def document_to_podcast(
    document_url: str,
    file_type: str = None,
    audio_format: str = None,
    host_name: str = None,
    cohost_name: str = None,
    host_voice_profile: str = None,
    cohost_voice_profile: str = None,
    text_to_text_model: str = None,
    text_to_speech_model: str = None,
):
    """Convert a document to a podcast.

    This pipeline downloads a document, processes it, converts it to a script,
    and finally converts the script to speech (podcast).

    Args:
        :param document_url: Path to the input document.
        :param file_type: The file type of the input document. e.g. .html, .txt, .pdf.
        :param audio_format: Output podcast file type .e.g. WAV, MP3.
        :param host_name: Name of the host.
        :param cohost_name: Name of the co-host.
        :param host_voice_profile: Voice profile for the host.
        :param cohost_voice_profile: Voice profile for the co-host.
        :param text_to_text_model: The text-to-speech model to use for script writing.
        :param text_to_speech_model: The text-to-speech model to use for performing the podcast.
    """
    download_document_step = download_document(document_url=document_url)
    download_document_step.set_caching_options(False)

    process_data_step = transform_document(
        file_path=download_document_step.outputs['downloaded_file_path'],
        file_type=file_type,
    ).after(download_document_step)
    process_data_step.set_caching_options(False)

    scriptwriter_step = scriptwriter(
        processed_document=process_data_step.outputs['processed_document'],
        host_name=host_name,
        cohost_name=cohost_name,
        model=text_to_text_model,
    ).after(process_data_step)
    scriptwriter_step.set_accelerator_type("nvidia.com/gpu")
    scriptwriter_step.set_accelerator_limit(1)
    scriptwriter_step.set_caching_options(False)

    performer_step = performer(
        podcast_script=scriptwriter_step.outputs['podcast_script'],
        host_voice_profile=host_voice_profile,
        cohost_voice_profile=cohost_voice_profile,
        model=text_to_speech_model,
        audio_format=audio_format,
    ).after(scriptwriter_step)
    performer_step.set_accelerator_type("nvidia.com/gpu")
    performer_step.set_accelerator_limit(1)
    performer_step.set_caching_options(False)


if __name__ == "__main__":
    compiler.Compiler().compile(document_to_podcast, package_path='document_to_podcast.yaml')